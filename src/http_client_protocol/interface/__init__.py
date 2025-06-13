"""Interface definitions for the HTTP client protocol package."""

__all__ = [
    "AsyncHTTPClientInterface",
    "HTTPClientInterface",
    "HTTPResponseInterface",
    "HeadersType",
]

from ._http import (
    AsyncHTTPClientInterface,
    HeadersType,
    HTTPClientInterface,
    HTTPResponseInterface,
)
