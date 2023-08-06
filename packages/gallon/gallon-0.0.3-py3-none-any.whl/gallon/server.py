"""Gallon server"""
import functools
import logging
import os
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any, Callable, NamedTuple, Optional, cast

from .helpers import make_response, setup_logger
from .objects import Request, Response


class GallonRoute(NamedTuple):
    """Route data model"""

    method: str
    path: str


class GallonRouter:
    """A simple router"""

    def __init__(self):
        self.routes = {}
        self.middleware = []

    def route(self, method: str, path: str):
        """Register a route"""

        def decorator(handler: Callable):
            self.routes[(method, path)] = handler
            return handler

        return decorator

    def get_handler(self, method: str, path: str):
        """Return a handler for a route"""
        return self.routes.get((method, path))


class GallonHandler(SimpleHTTPRequestHandler):
    """HTTP request handler"""

    router = GallonRouter()
    
    def handle_request(self, method: str):
        """Handle a request"""
        handler = self.router.get_handler(method, self.path)
        if handler is not None:
            # Get middleware from route if it exists
            request = self.get_request(method)
            raw_response = handler(request)  # handler's return value
            response = make_response(
                raw_response
            )  # use make_response to format it properly
            self.send_response(response.status)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(response.body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Access-Control-Max-Age", "86400")
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
            body=cast(Optional[str], body),
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
        super().__init__((host, port), GallonHandler)
        self.handler = GallonHandler
        self.logger = logging.getLogger(__name__)
    
    def route(self, method: str, path: str):
        """Register a route"""
        def decorator(handler: Callable):
            self.handler.router.route(method, path)(handler)
            return handler
        return decorator

    
    def get(self, path: str):
        """Register a GET route"""
        return self.route("GET", path)
    
    def post(self, path: str):
        """Register a POST route"""
        return self.route("POST", path)
    def put(self, path: str):
        """Register a PUT route"""
        return self.route("PUT", path)

    def delete(self, path: str):
        """Register a DELETE route"""
        return self.route("DELETE", path)

    def run(self):
        """Run the server"""
        self.logger = setup_logger()
        self.logger.info("Starting server at http://%s:%s", *self.server_address)
        self.logger.info("Press Ctrl+C to stop the server")

        # Monitor for file changes in a separate thread
        self.file_change_monitor_thread = threading.Thread(target=self.monitor_files)
        self.file_change_monitor_thread.start()

        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.logger.info("Stopping server")
            self.shutdown()
            self.server_close()
            self.logger.info("Server stopped")
        finally:
            self.logger.handlers.clear()

    def monitor_files(self):
        """Monitor for changes in Python files and restart the server if a change is detected"""
        path_to_watch = "."  # Directory to monitor
        file_modification_times = self.track_files(path_to_watch)

        while True:
            time.sleep(1)
            new_file_modification_times = self.track_files(path_to_watch)
            if new_file_modification_times != file_modification_times:
                self.logger.info("Change detected, restarting server.")
                self.restart()
                break  # Exit the monitoring thread

    @staticmethod
    def track_files(path):
        """Get the modification times for all Python files in the specified path"""
        file_modification_times = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    file_modification_times[file_path] = os.path.getmtime(file_path)
        return file_modification_times

    def restart(self):
        """Restart the server"""
        self.logger.info("Restarting server")
        self.shutdown()
        self.server_close()
        os.execv(sys.executable, ['python'] + sys.argv)  # Start a new instance of the current script

        
        