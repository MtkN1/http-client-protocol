from __future__ import annotations

import urllib.request
from typing import TYPE_CHECKING

import pytest

import http_client_protocol.backends.urllib

if TYPE_CHECKING:
    from aiohttp.test_utils import TestServer

    from http_client_protocol.interface import HTTPClientInterface


def test_urllib_type() -> None:
    def _handle_http_client(_http_client: HTTPClientInterface, /) -> None: ...

    client = http_client_protocol.backends.urllib.HTTPClient()
    _handle_http_client(client)


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
