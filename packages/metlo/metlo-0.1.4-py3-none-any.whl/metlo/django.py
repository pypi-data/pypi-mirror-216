from urllib.parse import urlparse
import logging
import metlo_python_agent_bindings_common
import json

from django.conf import settings
from django.http import HttpResponse

from metlo.utils import map_log_level_to_string, DEFAULT_BODY_SIZE


def get_src_ip(request):
    return (
        request.META.get("REMOTE_ADDR")
        if "1.0.0.127.in-addr.arpa" not in request.META.get("REMOTE_ADDR")
        else "localhost"
    )


def get_dest_ip(request):
    return (
        request.META.get("SERVER_NAME")
        if "1.0.0.127.in-addr.arpa" not in request.META.get("SERVER_NAME")
        else "localhost"
    )


def get_src_port(request):
    source_port = None
    try:
        source_port = request.environ["wsgi.input"].stream.raw._sock.getpeername()[1]
    except:
        source_port = request.META.get("REMOTE_PORT")
    return int(source_port)


"""
Accepts levels
 - Error  (40)
 - WARN   (30)
 - INFO   (20)
 - DEBUG  (10)
 - TRACE  (5)
"""


class MetloDjango(object):
    def compile_request(self, request):
        params = request.GET if request.method == "GET" else request.POST
        return {
            "url": {
                "host": request._current_scheme_host
                if request._current_scheme_host
                else get_src_ip(request),
                "path": request.path,
                "parameters": list(
                    map(
                        lambda x: {"name": x[0], "value": x[1]},
                        params.items(),
                    )
                ),
            },
            "headers": list(
                map(
                    lambda x: {"name": x[0], "value": x[1]},
                    request.headers.items(),
                )
            ),
            "body": request.body.decode("utf-8")[: self.MAX_BODY],
            "method": request.method,
            "user": self.get_user(request) if self.get_user else None,
        }

    def compile_meta(self, request):
        return {
            "environment": "production",
            "incoming": True,
            "source": get_src_ip(request),
            "sourcePort": get_src_port(request),
            "destination": get_dest_ip(request),
            "destinationPort": int(request.META.get("SERVER_PORT")),
            "metloSource": "python/django",
        }

    def compile_response(self, response):
        res_body: str = response.content.decode("utf-8")
        return {
            "status": response.status_code,
            "headers": list(
                map(
                    lambda x: {"name": x[0], "value": x[1]},
                    response.headers.items(),
                )
            ),
            "body": res_body[: self.MAX_BODY],
        }

    def __init__(self, get_response):
        """
        Middleware for Django to communicate with METLO
        :param get_response: Automatically populated by django
        """
        self.get_response = get_response
        self.logger = logging.getLogger("metlo")
        ch = logging.StreamHandler()

        level = settings.METLO_CONFIG.get("LOG_LEVEL", logging.INFO)

        ch.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z",
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.disabled = settings.METLO_CONFIG.get("DISABLED", False)
        assert (
            settings.METLO_CONFIG.get("METLO_HOST") is not None
        ), "METLO_CONFIG is missing METLO_HOST attribute"
        assert (
            settings.METLO_CONFIG.get("API_KEY") is not None
        ), "METLO_CONFIG is missing API_KEY attribute"
        assert urlparse(settings.METLO_CONFIG.get("METLO_HOST")).scheme in [
            "http",
            "https",
        ], f"Metlo for Django has invalid host scheme. Host must be in format http[s]://<host>"

        self.host = settings.METLO_CONFIG["METLO_HOST"]
        self.key = settings.METLO_CONFIG["API_KEY"]
        params = {}

        _settings = settings.METLO_CONFIG
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

    def __call__(self, request):
        if self.can_start:
            compiledRequest = self.compile_request(request)
            compiledMeta = self.compile_meta(request)
            if metlo_python_agent_bindings_common.block_trace(
                json.dumps(compiledRequest), json.dumps(compiledMeta)
            ):
                if self.reject_response:
                    return self.reject_response(request)
                else:
                    return HttpResponse("Forbidden", status=403)
        response = self.get_response(request)
        if not self.disabled and self.can_start:
            try:
                data = {
                    "request": compiledRequest,
                    "response": self.compile_response(response),
                    "meta": compiledMeta,
                }
                metlo_python_agent_bindings_common.process_trace(json.dumps(data))
            except Exception as e:
                self.logger.debug(e)
        return response

    def process_exception(self, request, exception):
        return None
