from __future__ import annotations

import contextlib
import urllib.request
from typing import TYPE_CHECKING

import httpx
import pytest

import http_client_protocol.backends.httpx
import http_client_protocol.backends.urllib

if TYPE_CHECKING:
    from collections.abc import Callable

    from aiohttp.test_utils import TestServer

    from http_client_protocol.interface import (
        AsyncHTTPClientInterface,
        HTTPClientInterface,
    )


def test_http_client_type() -> None:
    def _handle_http_client(_http_client: HTTPClientInterface, /) -> None: ...

    urllib_client = http_client_protocol.backends.urllib.HTTPClient()
    _handle_http_client(urllib_client)

    httpx_client = http_client_protocol.backends.httpx.HTTPClient()
    _handle_http_client(httpx_client)


def test_async_http_client_type() -> None:
    def _handle_http_client(_http_client: AsyncHTTPClientInterface, /) -> None: ...

    httpx_client = http_client_protocol.backends.httpx.AsyncHTTPClient()
    _handle_http_client(httpx_client)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (("/hello/200", None), 200),
        (("/hello/404", None), 404),
        (("/hello/500", urllib.request.build_opener()), 500),
    ],
)
def test_urllib_client(
    testing_server: TestServer,
    test_input: tuple[str, urllib.request.OpenerDirector | None],
    expected: int,
) -> None:
    path, opener = test_input
    url = str(testing_server.make_url(path))

    client = http_client_protocol.backends.urllib.HTTPClient(opener)
    response = client.request("GET", url)

    assert response.status_code == expected
    assert response.content == b"Hello, world"


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (("/hello/200", None), 200),
        (("/hello/404", None), 404),
        (("/hello/500", lambda: httpx.Client()), 500),
    ],
)
def test_httpx_client(
    testing_server: TestServer,
    test_input: tuple[str, Callable[..., httpx.Client] | None],
    expected: int,
) -> None:
    path, client_factory = test_input
    url = str(testing_server.make_url(path))

    cm = contextlib.nullcontext() if client_factory is None else client_factory()
    with cm as raw_client:
        client = http_client_protocol.backends.httpx.HTTPClient(raw_client)
        response = client.request("GET", url)

    assert response.status_code == expected
    assert response.content == b"Hello, world"


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (("/hello/200", None), 200),
        (("/hello/404", None), 404),
        (("/hello/500", lambda: httpx.AsyncClient()), 500),
    ],
)
async def test_httpx_async_client(
    testing_server: TestServer,
    test_input: tuple[str, Callable[..., httpx.AsyncClient] | None],
    expected: int,
) -> None:
    path, client_factory = test_input
    url = str(testing_server.make_url(path))

    cm = contextlib.nullcontext() if client_factory is None else client_factory()
    async with cm as raw_client:
        client = http_client_protocol.backends.httpx.AsyncHTTPClient(raw_client)
        response = await client.request("GET", url)

    assert response.status_code == expected
    assert response.content == b"Hello, world"
