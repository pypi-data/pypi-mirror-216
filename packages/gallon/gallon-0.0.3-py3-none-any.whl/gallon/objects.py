"""Base Request and Response Objects"""
from typing import Any, Optional, cast
from urllib.parse import parse_qs, urlparse

from typing_extensions import override

from .data import GallonModel, Json, field, loads

JSON_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Content-Type": "application/json",
}

class Request(GallonModel):
    """
    Request Object
    Interface that defines the shape of incoming http requests
    """

    url: str = field(...)
    method: str = field(...)
    headers: dict = field(JSON_CORS_HEADERS)
    body: str = field(None)

    @override
    def json(self, exclude_none: bool = True):
        """
        Convert and return the body as a JSON object if Content-Type is application/json.

        Returns:
            None: if body is empty or Content-Type is not application/json.
            Json: the body as a JSON object.
        """
        if self.body is None:
            return None
        if self.headers.get("Content-Type") != "application/json":
            return None
        return cast(Json, loads(self.body))

    @property
    def content_type(self):
        """
        Get the value of the Content-Type header.

        Returns:
            str: the value of the Content-Type header.
        """
        return self.headers.get("Content-Type")

    @property
    def content_length(self):
        """
        Get the value of the Content-Length header.
        If Content-Length is not set, it calculates the length of the body and sets the header accordingly.

        Returns:
            str: the value of the Content-Length header.
        """
        if self.headers.get("Content-Length") is None:
            self.headers["Content-Length"] = str(len(self.body or ""))
        assert self.headers.get("Content-Length") == str(len(self.body or ""))
        return self.headers.get("Content-Length")

    @property
    def query(self):
        """
        Parse and return the query parameters from the URL.

        Returns:
            dict: the query parameters.
        """
        return {k: v[0] for k, v in parse_qs(urlparse(self.url).query).items()}

    @property
    def path(self):
        """
        Extract and return the path from the URL.

        Returns:
            str: the path of the URL.
        """
        return urlparse(self.url).path


class Response(GallonModel):
    """
    Response Object
    Interface that defines the shape of outgoing http responses
    """

    status: int = field(...)
    headers: dict = field(...)
    body: Optional[str] = field(None)

    @override
    def json(self, exclude_none: bool = True):
        """
        Convert and return the body as a JSON object.

        Returns:
            None: if body is empty.
            Json: the body as a JSON object.
        """
        if self.body is None:
            return None
        return cast(Json, loads(self.body))

    @property
    def content_type(self):
        """
        Get the value of the Content-Type header.

        Returns:
            str: the value of the Content-Type header.
        """
        return self.headers.get("Content-Type")

    @property
    def content_length(self):
        """
        Get the value of the Content-Length header.
        If Content-Length is not set, it calculates the length of the body and sets the header accordingly.

        Returns:
            str: the value of the Content-Length header.
        """
        if self.headers.get("Content-Length") is None:
            self.headers["Content-Length"] = str(len(self.body or ""))
        assert self.headers.get("Content-Length") == str(len(self.body or ""))
        return self.headers.get("Content-Length")
