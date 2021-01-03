import base64
import json
import http.client as httplib
from twisted.internet import defer
import urllib.parse as urlparse
from logzero import logger

from .exceptions import JsonRpcException


class Rpc(object):
    __id_count = 0

    def __init__(self, url, timeout=30, user_agent="Kryptos/0.0.1", service_name=None, connection=None):
        if isinstance(url, str):
            self.__url = urlparse.urlparse(f"{url}")
        else:
            self.__url = url

        # Check url
        if self.__url.port is None:
            port = 80
        else:
            port = self.__url.port

        self.__auth_header = "Basic {}".format(
            self.__bytes_to_str(base64.b64encode(self.__str_to_bytes(f"{self.__url.username}:{self.__url.password}"))))
        self.__user_agent = user_agent
        self.__timeout = timeout
        self.__service_name = service_name

        if connection is None:
            self.__connection = httplib.HTTPConnection(self.__url.hostname, port, timeout)
        else:
            self.__connection = connection

    @staticmethod
    def __str_to_bytes(string):
        if isinstance(string, str):
            return string.encode("utf-8")

    @staticmethod
    def __bytes_to_str(byts):
        if isinstance(byts, bytes):
            return byts.decode("utf-8")

    def __getattr__(self, item):
        if item.startswith("__") and item.endswith("__"):
            raise AttributeError

        if self.__service_name is not None:
            item = f"{self.__service_name}.{item}"
        return Rpc(url=self.__url, service_name=item, timeout=self.__timeout, connection=self.__connection)

    @defer.inlineCallbacks
    def __call__(self, *args, **kwargs):
        Rpc.__id_count += 1

        logger.debug(
            f"#{Rpc.__id_count} -> "
            f"{self.__url.scheme}://{self.__url.username}:***@{self.__url.hostname}:{self.__url.port} -> {self.__service_name} {json.dumps(args)}")

        post_data = json.dumps({
            "version": "2.0",
            "method": self.__service_name,
            "params": args,
            "id": Rpc.__id_count
        })

        try:
            self.__connection.request(method="POST", url=self.__url.path, body=post_data,
                                      headers={"Host": self.__url.hostname,
                                               "User-Agent": self.__user_agent,
                                               "Authorization": self.__auth_header,
                                               "Content-Type": "application/json"})
            self.__connection.sock.settimeout(self.__timeout)
            response = self._get_response()
            if response.get("error") is not None:
                raise JsonRpcException(response["error"])
            elif "result" not in response:
                raise JsonRpcException({"code": -343, "message": "Missing JSON-RPC result"})

            defer.returnValue((yield response["result"]))
        except Exception as e:
            logger.error(e)
            self.__connection.close()
            return None

    def _get_response(self):
        http_response = self.__connection.getresponse()

        if http_response is None:
            raise JsonRpcException({"code": -342, "message": "Missing HTTP response from server"})

        content_type = http_response.getheader("Content-Type")
        if not content_type.startswith("application/json"):
            raise JsonRpcException({"code": -342, "message": f"{content_type} HTTP response with "
                                                             f"{http_response.status} {http_response.reason}"})

        response_data = self.__bytes_to_str(http_response.read())
        response = json.loads(response_data)

        if "error" in response and response["error"] is None:
            logger.debug(f"#{response['id']} <- {json.dumps(response['result'])}")
        else:
            logger.debug(f"<-- {response_data}")
        return response
