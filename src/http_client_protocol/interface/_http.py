from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, TypeAlias

HeadersType: TypeAlias = Mapping[str, str]


class HTTPResponseInterface(Protocol):
    status_code: int
    headers: HeadersType
    content: bytes


class HTTPClientInterface(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: HeadersType | None = None,
        content: bytes | None = None,
    ) -> HTTPResponseInterface: ...


class AsyncHTTPClientInterface(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: HeadersType | None = None,
        content: bytes | None = None,
    ) -> HTTPResponseInterface: ...
