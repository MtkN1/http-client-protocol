from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from http_client_protocol.backends.dataclasses import HTTPResponse
from http_client_protocol.interface import (
    AsyncHTTPClientInterface,
    HeadersType,
    HTTPClientInterface,
    HTTPResponseInterface,
)

if TYPE_CHECKING:
    import httpx


class HTTPClient(HTTPClientInterface):
    """HTTP client implementation using httpx for sending HTTP requests."""

    def __init__(
        self,
        client: httpx.Client | None = None,
        /,
    ) -> None:
        self._client = client

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: HeadersType | None = None,
        content: bytes | None = None,
    ) -> HTTPResponseInterface:
        if self._client is None:
            import httpx

            cm = httpx.Client()
        else:
            cm = contextlib.nullcontext(self._client)

        with cm as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers,
                content=content,
            )
        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
        )


class AsyncHTTPClient(AsyncHTTPClientInterface):
    """Asynchronous HTTP client implementation using httpx for sending HTTP requests."""

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        /,
    ) -> None:
        self._client = client

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: HeadersType | None = None,
        content: bytes | None = None,
    ) -> HTTPResponseInterface:
        if self._client is None:
            import httpx

            cm = httpx.AsyncClient()
        else:
            cm = contextlib.nullcontext(self._client)

        async with cm as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=content,
            )
        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
        )
