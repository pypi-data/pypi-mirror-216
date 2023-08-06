import json
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request
from urllib.parse import urlparse
import logging

from flask import request

import metlo_python_agent_bindings_common

from metlo.utils import DEFAULT_BODY_SIZE, map_log_level_to_string

endpoint = "api/v1/log-request/single"


class MetloFlask:
    def get_dst_host(self, request):
        return (
            request.environ.get("HTTP_HOST")
            or request.environ.get("HTTP_X_FORWARDED_FOR")
            or request.environ.get("REMOTE_ADDR")
        )

    def compile_request(self, request):
        return {
            "url": {
                "host": self.get_dst_host(request),
                "path": request.path,
                "parameters": list(
                    map(
                        lambda x: {"name": x[0], "value": x[1]},
                        request.args.items(),
                    )
                ),
            },
            "headers": list(
                map(
                    lambda x: {"name": x[0], "value": x[1]},
                    request.headers.items(),
                )
            ),
            "body": request.data.decode("utf-8"),
            "method": request.method,
        }

    def compile_response(self, response):
        return {
            "status": response.status_code,
            "headers": list(
                map(
                    lambda x: {"name": x[0], "value": x[1]},
                    response.headers.items(),
                )
            ),
            "body": response.data.decode("utf-8"),
        }

    def compile_meta(self, request):
        return {
            "environment": "production",
            "incoming": True,
            "source": request.environ.get("HTTP_X_FORWARDED_FOR")
            or request.environ.get("REMOTE_ADDR"),
            "sourcePort": int(request.environ.get("REMOTE_PORT")),
            "destination": request.environ.get("SERVER_NAME"),
            "destinationPort": int(request.environ.get("SERVER_PORT")),
            "metloSource": "python/flask",
        }

    def __init__(self, app, metlo_host: str, metlo_api_key: str, **kwargs):
        """
        :param app: Instance of Flask app
        :param metlo_host: Publicly accessible address of Metlo Collector
        :param metlo_api_key: Metlo API Key
        :param kwargs: optional parameter containing worker count for communicating with metlo
        """
        self.app = app

        self.disabled = kwargs.get("disabled", False)
        self.logger = logging.getLogger("metlo")
        ch = logging.StreamHandler()

        level = kwargs.get("LOG_LEVEL", logging.INFO)

        ch.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z",
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        assert (
            metlo_host is not None
        ), "Metlo for FLASK __init__ is missing metlo_host parameter"
        assert (
            metlo_api_key is not None
        ), "Metlo for FLASK __init__ is missing metlo_api_key parameter"
        assert urlparse(metlo_host).scheme in [
            "http",
            "https",
        ], f"Metlo for FLASK has invalid host scheme. Host must be in format http[s]://example.com"

        self.host = metlo_host
        self.key = metlo_api_key
        params = {}

        _settings = kwargs
        shouldStart = True

        params["log_level"] = map_log_level_to_string(level)

        # Collector Port
        if "COLLECTOR_PORT" in _settings:
            if (_settings["COLLECTOR_PORT"] is not None) and isinstance(
                _settings["COLLECTOR_PORT"], int
            ):
                params["collector_port"] = _settings["COLLECTOR_PORT"]
            else:

                self.logger.error(
                    "Metlo COLLECTOR_PORT arg is incorrectly specified. Metlo will not start"
                )
                shouldStart = False

        # Backend Port
        if "BACKEND_PORT" in _settings:
            if (_settings["BACKEND_PORT"] is not None) and isinstance(
                _settings["BACKEND_PORT"], int
            ):
                params["backend_port"] = _settings["BACKEND_PORT"]
            else:
                self.logger.error(
                    "Metlo BACKEND_PORT arg is incorrectly specified. Metlo will not start"
                )
                shouldStart = False

        # Encryption Key
        if "ENCRYPTION_KEY" in _settings:
            if (_settings["ENCRYPTION_KEY"] is not None) and isinstance(
                _settings["ENCRYPTION_KEY"], str
            ):
                params["encryption_key"] = _settings["ENCRYPTION_KEY"]
            else:
                self.logger.error(
                    "Metlo ENCRYPTION_KEY arg is incorrectly specified. Metlo will not start"
                )
                shouldStart = False

        # Get User
        if "GET_USER" in _settings and callable(_settings["GET_USER"]):
            self.get_user = _settings["GET_USER"]
        else:
            self.logger.debug(
                "Metlo GET_USER arg is incorrectly specified or unspecified"
            )
            self.get_user = None

        # Reject Response
        if "REJECT_RESPONSE" in _settings and callable(_settings["REJECT_RESPONSE"]):
            self.reject_response = _settings["REJECT_RESPONSE"]
        else:
            self.logger.debug(
                "Metlo REJECT_RESPONSE arg is incorrectly specified or unspecified"
            )
            self.reject_response = None

        if "MAX_BODY" in _settings and isinstance(_settings["MAX_BODY"], int):
            self.MAX_BODY = _settings["MAX_BODY"]
        else:
            self.MAX_BODY = DEFAULT_BODY_SIZE

        self.can_start = False
        try:
            if shouldStart:
                metlo_python_agent_bindings_common.setup(self.host, self.key, **params)
                self.can_start = True
        except Exception as e:
            self.logger.error(e)

        if not self.disabled and self.can_start:

            @app.before_request
            def function():
                try:
                    compiledRequest = json.dumps(self.compile_request(request))
                    compiledMeta = json.dumps(self.compile_meta(request))
                    if metlo_python_agent_bindings_common.block_trace(
                        compiledRequest, compiledMeta
                    ):
                        if self.reject_response:
                            return self.reject_response(request)
                        else:
                            return 403
                except Exception as e:
                    self.logger.debug(e)

            @app.after_request
            def function(response, *args, **kwargs):
                try:
                    data = {
                        "request": self.compile_request(request),
                        "response": self.compile_response(response),
                        "meta": self.compile_meta(request),
                    }
                    metlo_python_agent_bindings_common.process_trace(json.dumps(data))
                except Exception as e:
                    self.logger.debug(e)
                return response
