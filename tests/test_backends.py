from __future__ import annotations

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
        ("/hello/200", 200),
        ("/hello/404", 404),
        ("/hello/500", 500),
    ],
)
def test_http_client(
    testing_server: TestServer, test_input: str, expected: int
) -> None:
    url = str(testing_server.make_url(test_input))

    client = http_client_protocol.backends.urllib.HTTPClient()
    response = client.request("GET", url)

    assert response.status_code == expected
    assert response.content == b"Hello, world"
