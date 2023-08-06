"""Gallon server"""
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Callable, NamedTuple

from .helpers import make_response
from .objects import Request


class Route(NamedTuple):
    """Route data model"""

    method: str
    path: str


class Router:
    """A simple router"""

    def __init__(self):
        self.routes = {}

    def route(self, method: str, path: str):
        """Register a route"""

        def decorator(handler: Callable):
            self.routes[(method, path)] = handler
            return handler

        return decorator

    def get_handler(self, method: str, path: str):
        """Return a handler for a route"""
        return self.routes.get((method, path))


class Handler(SimpleHTTPRequestHandler):
    """HTTP request handler"""

    router = Router()

    def handle_request(self, method: str):
        """Handle a request"""
        handler = self.router.get_handler(method, self.path)
        if handler is not None:
            request = self.get_request(method)
            raw_response = handler(request)  # handler's return value
            response = make_response(
                raw_response
            )  # use make_response to format it properly
            self.send_response(response.status)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            assert response.body is not None
            self.wfile.write(response.body.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    def get_request(self, method: str):
        """Return the request"""
        headers = {key: value for key, value in self.headers.items()}
        body = self.get_body()
        return Request(
            url=self.path,
            method=method,
            headers=headers,
            body=body,
        )

    def get_body(self):
        """Return the body"""
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            return None
        length = int(content_length)
        return self.rfile.read(length).decode("utf-8")

    def process_request(self, request: Request, handler: Callable):
        """Handle a request"""
        response = handler(request)
        return make_response(response)

    def do_GET(self):
        """Handle a GET request"""
        self.handle_request("GET")

    def do_POST(self):
        """Handle a POST request"""
        self.handle_request("POST")

    def do_PUT(self):
        """Handle a PUT request"""
        self.handle_request("PUT")

    def do_DELETE(self):
        """Handle a DELETE request"""
        self.handle_request("DELETE")


class Gallon(HTTPServer):
    """
    A Zero-Dependency Python Micro Framework
    Features:
    - Routing
    - Request and Response objects
    - JSON support
    - Data validation
    - Decorators
    - Static files
    """

    def __init__(self, host: str = "localhost", port: int = 8000):
        super().__init__((host, port), Handler)
        self.handler = Handler
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def get(self, path: str):
        """Register a GET route"""
        return self.handler.router.route("GET", path)

    def post(self, path: str):
        """Register a POST route"""
        return self.handler.router.route("POST", path)

    def put(self, path: str):
        """Register a PUT route"""
        return self.handler.router.route("PUT", path)

    def delete(self, path: str):
        """Register a DELETE route"""
        return self.handler.router.route("DELETE", path)

    def run(self):
        """Run the server"""
        self.logger.info(
            "%s running on %s",
            self.__class__.__name__,
            f"http://{self.server_name}:{self.server_port}",
        )
