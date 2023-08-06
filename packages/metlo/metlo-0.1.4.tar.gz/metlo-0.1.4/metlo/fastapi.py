import json
from urllib.parse import urlparse
import logging
import typing
from inspect import iscoroutinefunction

from fastapi.responses import PlainTextResponse
from starlette.types import Message, Scope, Receive, Send
from starlette.responses import Response

from metlo.utils import map_log_level_to_string, DEFAULT_BODY_SIZE

import metlo_python_agent_bindings_common


def get_src_ip(scope: Scope):
    src_ip = ""
    try:
        src_ip = (
            scope["client"][0]
            if "1.0.0.127.in-addr.arpa" not in scope["client"][0]
            else "localhost"
        )
    except:
        pass
    return src_ip


def get_dest_ip(scope: Scope):
    dest_ip = ""
    try:
        dest_ip = scope["server"][0]
    except:
        pass
    return dest_ip


def get_src_port(scope: Scope):
    source_port = "0"
    try:
        source_port = scope["client"][1] if scope["client"][1] is not None else "0"
    except:
        source_port = "0"
    return int(source_port)


def get_dest_port(scope: Scope):
    dest_port = "0"
    try:
        dest_port = scope["server"][1] if scope["server"][1] is not None else "0"
    except:
        source_port = "0"
    return int(dest_port)


def get_key(key):
    return f"metlo_{key}"


def check_key_in_state(key: str, scope: Scope):
    return get_key(key) in scope["state"]


def get_value_from_state(key: str, scope: Scope, default=None):
    if check_key_in_state(key, scope):
        return scope["state"][get_key(key)]
    else:
        return default


def set_value_in_state(key: str, data: typing.Any, scope: Scope):
    scope["state"][get_key(key)] = data


class ASGIMiddleware(object):
    instance = None

    def __init__(self, app, host, api_key, **kwargs):
        if ASGIMiddleware.instance is None:
            ASGIMiddleware.instance = MetaASGIMiddleware(app, host, api_key, **kwargs)
        else:
            ASGIMiddleware.instance.logger.debug("Attempted multiple init")

    async def __call__(self, scope, receive, send):
        return await ASGIMiddleware.instance(scope, receive, send)


class MetaASGIMiddleware(object):
    def compile_request(self, scope: Scope):
        user = None
        req_body = ""
        try:
            user = self.get_user(scope) if self.get_user is not None else None
        except Exception as e:
            self.logger.error("Error obtaining user info from function")
            self.logger.error(e)
            user = None
        try:
            req_body = (
                get_value_from_state("req_body", scope)
                if (
                    check_key_in_state("req_body", scope)
                    and isinstance(get_value_from_state("req_body", scope), bytes)
                )
                else b""
            ).decode()
        except Exception as e:
            self.logger.debug("Error decoding request body")
            self.logger.debug(e)
            req_body = ""

        return {
            "url": {
                "host": self.api_host
                if self.api_host is not None
                else f"{get_dest_ip(scope)}:{get_dest_port(scope)}",
                "path": scope["path"],
                "parameters": list(
                    map(
                        lambda x: {"name": x[0], "value": x[1]},
                        [
                            x.split("=")
                            for x in scope["query_string"].decode().split("&")
                            if x
                        ],
                    )
                ),
            }
            if ("query_string" in scope and isinstance(scope["query_string"], bytes))
            else [],
            "headers": list(
                map(
                    lambda x: {"name": x[0].decode(), "value": x[1].decode()},
                    [
                        x
                        for x in scope["headers"]
                        if isinstance(x[0], bytes) and isinstance(x[1], bytes)
                    ],
                )
            )
            if ("headers" in scope and isinstance(scope["headers"], list))
            else [],
            "body": req_body,
            "method": scope["method"],
            "user": user,
        }

    def compile_meta(self, scope: Scope):
        return {
            "environment": "production",
            "incoming": True,
            "source": get_src_ip(scope),
            "sourcePort": get_src_port(scope),
            "destination": get_dest_ip(scope),
            "destinationPort": get_dest_port(scope),
            "metloSource": "python/fastapi",
        }

    def compile_response(self, scope: Scope):
        res_body: str = ""
        try:
            res_body = (
                get_value_from_state("res_body", scope, "")
                if check_key_in_state("res_body", scope)
                and isinstance(get_value_from_state("res_body", scope), bytes)
                else b""
            ).decode()
        except Exception as e:
            self.logger.debug("Error decoding response body")
            self.logger.debug(e)
            res_body = ""
        return {
            "status": get_value_from_state("status", scope, []),
            "headers": list(
                map(
                    lambda x: {"name": x[0].decode(), "value": x[1].decode()},
                    [
                        x
                        for x in get_value_from_state("res_headers", scope, [])
                        if isinstance(x[0], bytes) and isinstance(x[1], bytes)
                    ],
                )
            ),
            "body": res_body,
        }

    def check_blocking(self, scope: Scope):
        try:
            self.logger.debug("Checking for blocking")
            compiledRequest = self.compile_request(scope)
            compiledMeta = self.compile_meta(scope)
            will_reject = metlo_python_agent_bindings_common.block_trace(
                json.dumps(compiledRequest), json.dumps(compiledMeta)
            )
            if will_reject:
                self.logger.debug("Will be rejecting response from Metlo")
            return will_reject
        except Exception as e:
            self.logger.error(e)
            return False

    def process_trace(self, scope):
        try:
            compiledRequest = self.compile_request(scope)
            compiledMeta = self.compile_meta(scope)
            compiledResponse = self.compile_response(scope)
            metlo_python_agent_bindings_common.process_trace(
                json.dumps(
                    {
                        "request": compiledRequest,
                        "response": compiledResponse,
                        "meta": compiledMeta,
                    }
                )
            )
            self.logger.debug("Sent trace")
        except Exception as e:
            self.logger.error("Encountered an error while sending trace to Metlo")
            self.logger.error(e)

    async def process_rejection(self, scope, receive, send):
        try:
            if self.reject_response is not None:
                return await self.reject_response(scope)(scope, receive, send)
            else:
                return await PlainTextResponse("Forbidden", 403)(scope, receive, send)
        except Exception as e:
            self.logger.error(
                "Encountered error while sending rejection response. Attempting to send default rejection response 403"
            )
            self.logger.error(e)
            return await PlainTextResponse("Forbidden", 403)(scope, receive, send)

    def __init__(self, app, host, api_key, **kwargs):
        self.app = app
        try:
            self.disabled = kwargs.get("disabled", False)
            if not (self.disabled):
                self.logger = logging.getLogger("metlo")
                ch = logging.StreamHandler()

                level = kwargs.get("log_level", logging.INFO)

                ch.setLevel(level)
                formatter = logging.Formatter(
                    "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s]  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %z",
                )
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

                assert (
                    host is not None
                ), "Metlo for FastAPI __init__ is missing host parameter"

                assert (
                    api_key is not None
                ), "Metlo for FASTAPI __init__ is missing api_key parameter"

                assert urlparse(host).scheme in [
                    "http",
                    "https",
                ], f"Metlo for FLASK has invalid host scheme. Host must be in format http[s]://example.com"

                self.host = host
                self.key = api_key
                params = {}

                settings = kwargs
                shouldStart = True

                params["log_level"] = map_log_level_to_string(level)

                # Collector Port
                if "collector_port" in settings:
                    if (settings["collector_port"] is not None) and isinstance(
                        settings["collector_port"], int
                    ):
                        params["collector_port"] = settings["collector_port"]
                    else:
                        self.logger.error(
                            "Metlo collector_port arg is incorrectly specified. Metlo will not start"
                        )
                        shouldStart = False

                # Backend Port
                if "backend_port" in settings:
                    if (settings["backend_port"] is not None) and isinstance(
                        settings["backend_port"], int
                    ):
                        params["backend_port"] = settings["backend_port"]
                    else:
                        self.logger.error(
                            "Metlo backend_port arg is incorrectly specified. Metlo will not start"
                        )
                        shouldStart = False

                # Encryption Key
                if "encryption_key" in settings:
                    if (settings["encryption_key"] is not None) and isinstance(
                        settings["encryption_key"], str
                    ):
                        params["encryption_key"] = settings["encryption_key"]
                    else:
                        self.logger.error(
                            "Metlo encryption_key arg is incorrectly specified. Metlo will not start"
                        )
                        shouldStart = False

                # API Host
                if "api_host" in settings:
                    if (settings["api_host"] is not None) and isinstance(
                        settings["api_host"], str
                    ):
                        self.api_host = settings["api_host"]
                    else:
                        self.api_host = None
                        self.logger.warn(
                            "Metlo api_host arg is incorrectly specified. Defaulting to value from connection"
                        )
                else:
                    self.api_host = None

                # Get User
                if "get_user" in settings:
                    if callable(settings["get_user"]) and not iscoroutinefunction(
                        settings["get_user"]
                    ):
                        self.get_user = settings["get_user"]
                    else:
                        self.logger.warn(
                            "Metlo get_user arg is incorrectly specified or unspecified. Require a synchronous function returning a string"
                        )
                        self.get_user = None
                else:
                    self.get_user = None

                # Reject Response
                if "reject_response" in settings:
                    if callable(
                        settings["reject_response"]
                    ) and not iscoroutinefunction(settings["reject_response"]):
                        self.reject_response = settings["reject_response"]
                    else:
                        self.logger.warn(
                            "Metlo reject_response arg is incorrectly specified or unspecified. Require a synchronous function returning a Response subclass"
                        )
                        self.reject_response = None
                else:
                    self.reject_response = None

                if "max_body" in settings:
                    if isinstance(settings["max_body"], int):
                        self.max_body = settings["max_body"]
                    else:
                        self.logger.warn(
                            "Could not read passed body size. Metlo will be using the default body capture size"
                        )
                        self.max_body = DEFAULT_BODY_SIZE
                else:
                    self.max_body = DEFAULT_BODY_SIZE

                can_start = False
                try:
                    if shouldStart:
                        metlo_python_agent_bindings_common.setup(
                            self.host, self.key, **params
                        )
                        can_start = True
                except Exception as e:
                    self.logger.error(e)

                self.disabled = not (can_start)
        except Exception as e:
            print("Metlo encountered an error during initialization")
            print(e)
            self.disabled = True

    async def __call__(self, scope, receive, send):
        if not (self.disabled):

            async def rec_wrapper():
                return await self.receivefn(scope, receive, send)

            async def send_wrapper(message):
                await self.sendfn(scope, send, message)

            try:
                if "http" in scope["type"]:
                    if self.check_blocking(scope):
                        set_value_in_state("rejected", True, scope)
                        await self.process_rejection(scope, receive, send_wrapper)
                    else:
                        await self.app(scope, rec_wrapper, send_wrapper)
                    return
            except Exception as e:
                self.logger.error(
                    "Metlo encountered an error while checking for blocking requests"
                )
                self.logger.error(e)

        await self.app(scope, receive, send)

    async def receivefn(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Receive this part of the request body
        req = await receive()
        # Check if we're processing http requests, websockets are currently not supported
        if "http" in req["type"]:
            try:
                # If we have a body in the request, try adding it to cache
                if "body" in req:
                    # Check if we have stored req_body already
                    if check_key_in_state("req_body", scope):
                        # Get length of current body segment
                        curr_length = len(req["body"])
                        # How much can we store ?
                        remaining_buffer = max(self.max_body - curr_length, 0)
                        # We can store a non-zero amount
                        if remaining_buffer > 0:
                            # How much can we put into the buffer:
                            # - either the full buffer
                            # - or, the remaining length
                            copy_length = min(remaining_buffer, len(req["body"]))
                            # Set the value for length
                            set_value_in_state(
                                "req_len_stored",
                                get_value_from_state("req_len_stored", scope, 0)
                                + copy_length,
                                scope,
                            )
                            # Set the value for body buffer
                            set_value_in_state(
                                "req_body",
                                get_value_from_state("req_body", scope, b"")
                                + req["body"][:copy_length],
                                scope,
                            )
                    # No body stored yet, Lets put all the data available
                    else:
                        set_value_in_state(
                            "req_len_stored",
                            min(self.max_body, len(req["body"])),
                            scope,
                        )

                        set_value_in_state(
                            "req_body",
                            req["body"][: self.max_body],
                            scope,
                        )
                # We have no body in req, lets put a placeholder
                else:
                    set_value_in_state(
                        "req_len_stored",
                        0,
                        scope,
                    )

                    set_value_in_state(
                        "req_body",
                        b"",
                        scope,
                    )
            except Exception as e:
                self.logger.error(
                    "Encountered an error while processing http request. Processing as normal"
                )
                self.logger.error(e)
            return req
        else:
            return req

    async def sendfn(self, scope: Scope, send: Send, message: Message) -> None:
        if "http" in message["type"]:
            try:
                # We received http response start. Can record status and headers from this
                if message["type"] == "http.response.start":
                    set_value_in_state("status", message["status"], scope)
                    set_value_in_state("res_headers", message["headers"], scope)
                elif message["type"] == "http.response.body":
                    # If message has a body, then see if we can add body
                    if "body" in message:
                        # Have we already recorded some part of the response body ?
                        if check_key_in_state("res_body", scope):
                            # Get length of body currently stored
                            curr_length = get_value_from_state(
                                "res_len_stored", scope, 0
                            )
                            # Remaining space in the buffer
                            remaining_buffer = max(self.max_body - curr_length, 0)
                            # If remaining space in the buffer is more than zero, then try to add part of body to buffer
                            if remaining_buffer > 0:
                                # Figure out how much we can add to the buffer
                                copy_length = min(
                                    remaining_buffer, len(message["body"])
                                )
                                set_value_in_state(
                                    "res_len_stored",
                                    curr_length + copy_length,
                                    scope,
                                )
                                # Add decoded body to buffer
                                set_value_in_state(
                                    "res_body",
                                    get_value_from_state("res_body", scope)
                                    + message["body"][:copy_length],
                                    scope,
                                )
                            else:
                                # Buffer is full, do nothing
                                pass
                        # We haven't recorded any part of the body yet.
                        else:
                            # We can either fill the entire body or upto self.max_body
                            set_value_in_state(
                                "res_len_stored",
                                min(len(message["body"]), self.max_body),
                                scope,
                            )

                            # We want decoded bodies only
                            set_value_in_state(
                                "res_body",
                                message["body"][: self.max_body],
                                scope,
                            )

                    else:
                        # Somehow body is missing from message of type 'http.response.body'
                        set_value_in_state(
                            "res_len_stored",
                            0,
                            scope,
                        )

                        set_value_in_state(
                            "res_body",
                            "",
                            scope,
                        )
                    # There will always be at least one http.response.body event.
                    # We haven't capture response yet
                    if not check_key_in_state("response_captured", scope):
                        # Check if there's still more body
                        if "more_body" in message and message["more_body"]:
                            # Check if we have actually filled the body
                            if (
                                get_value_from_state("res_len_stored", scope, 0)
                                == self.max_body
                            ):
                                # Filled the body completely, Set the flag and process trace
                                set_value_in_state("response_capture", True, scope)
                                self.process_trace(scope)
                            else:
                                # We haven't filled the body yet and there's still more data to consume
                                pass
                        # There's no more data in the buffer and we haven't already processed the data.
                        else:
                            # Set the flag and process the trace
                            set_value_in_state("response_capture", True, scope)
                            self.process_trace(scope)
            except Exception as e:
                self.logger.error(
                    "Encountered an error while sending response. Processing as normal"
                )
                self.logger.error(e)
        return await send(message)
