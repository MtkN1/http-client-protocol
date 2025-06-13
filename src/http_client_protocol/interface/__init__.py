"""Interface definitions for the HTTP client protocol package."""

__all__ = [
    "HTTPClientInterface",
    "HTTPResponseInterface",
    "HeadersType",
]

from ._http import HeadersType, HTTPClientInterface, HTTPResponseInterface
