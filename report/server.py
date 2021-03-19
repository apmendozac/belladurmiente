from http.server import BaseHTTPRequestHandler
from report import Report
import json

class Server(BaseHTTPRequestHandler):
    """docstring for Sever."""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        instantClass = Report()
        a = instantClass.main()