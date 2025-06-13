from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer
from anyio import from_thread

if TYPE_CHECKING:
    from collections.abc import Generator

routes = web.RouteTableDef()


@routes.get("/hello")
@routes.get(r"/hello/{status:\d+}")
async def hello_200(request: web.Request) -> web.Response:
    status = int(request.match_info.get("status", "200"))
    return web.Response(text="Hello, world", status=status)


@pytest.fixture(scope="session")
def testing_server() -> Generator[TestServer]:
    app = web.Application()
    app.add_routes(routes)

    with (
        from_thread.start_blocking_portal(backend="asyncio") as portal,
        portal.wrap_async_context_manager(TestServer(app)) as server,
    ):
        assert isinstance(server, TestServer)
        yield server
