from __future__ import annotations

import urllib.error
import urllib.request
from typing import TYPE_CHECKING

from http_client_protocol.backends.dataclasses import HTTPResponse
from http_client_protocol.interface import (
    HeadersType,
    HTTPClientInterface,
    HTTPResponseInterface,
)

if TYPE_CHECKING:
    import http.client


class HTTPClient(HTTPClientInterface):
    """HTTP client implementation using urllib.request for sending HTTP requests."""

    def __init__(
        self,
        opener: urllib.request.OpenerDirector | None = None,
        /,
    ) -> None:
        if opener is None:
            opener = urllib.request.build_opener()
        self._opener = opener

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: HeadersType | None = None,
        content: bytes | None = None,
    ) -> HTTPResponseInterface:
        request = urllib.request.Request(  # noqa: S310
            url,
            data=content,
            headers=dict(headers or {}),
            method=method,
        )
        try:
            response: http.client.HTTPResponse
            with self._opener.open(request) as response:
                return HTTPResponse(
                    status_code=response.status,
                    headers=dict(response.getheaders()),
                    content=response.read(),
                )
        except urllib.error.HTTPError as e:
            return HTTPResponse(
                status_code=e.code,
                headers=dict(e.headers),
                content=e.fp.read(),
            )
