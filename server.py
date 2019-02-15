#!/usr/bin/python3

import http.server
import socketserver
import query
import json
import urllib.parse

PORT = 8000


class MyHTTPRequestHandler(http.server.CGIHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/raw/'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=UTF-8')
            self.end_headers()
            self.wfile.write(bytes(query.query(urllib.parse.unquote(self.path[5:]), raw=True), 'utf-8'))
        elif self.path.startswith('/json/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=UTF-8')
            self.end_headers()
            self.wfile.write(bytes(query.query(urllib.parse.unquote(self.path[6:]), raw=False), 'utf-8'))
        else:
            self.wfile.write(bytes(json.dumps({
                "result": "error"
            }), 'utf-8'))


Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
