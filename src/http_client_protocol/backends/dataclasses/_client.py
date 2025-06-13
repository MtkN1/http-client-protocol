from dataclasses import dataclass

from http_client_protocol.interface import HeadersType, HTTPResponseInterface


@dataclass
class HTTPResponse(HTTPResponseInterface):
    status_code: int
    headers: HeadersType
    content: bytes
