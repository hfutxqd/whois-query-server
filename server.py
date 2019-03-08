#!/usr/bin/python3

import http.server
import socketserver
import time

import query
import json
import urllib.parse
import os
import requests
from threading import Thread

PORT = 8000

CALLBACK_POST_URL = os.getenv('CALLBACK_POST_URL', None)


class MyHTTPRequestHandler(http.server.CGIHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/raw/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=UTF-8')
            self.end_headers()
            self.wfile.write(bytes(query.query(urllib.parse.unquote(self.path[5:]), raw=True), 'utf-8'))
        elif self.path.startswith('/json/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=UTF-8')
            self.end_headers()
            self.wfile.write(bytes(query.query(urllib.parse.unquote(self.path[6:]), raw=False), 'utf-8'))
        else:
            self.wfile.write(bytes(json.dumps({
                "result": "error"
            }), 'utf-8'))

    def do_POST(self):
        if self.path == '/json/post':
            try:
                print('got a post request')
                content_length = int(self.headers['Content-Length'])
                print('Content-Length: ' + str(content_length))
                body = self.rfile.read(content_length)
                # {
                #     "request_id": "sdfdfdf",
                #     "domains": []
                # }
                domains = json.loads(str(body, 'utf-8'))
                print(domains)
                if "domains" not in domains or "request_id" not in domains:
                    res_body = bytes(json.dumps({'code': '400'}), 'utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=UTF-8')
                    self.send_header('Content-Length', str(len(res_body)))
                    self.end_headers()
                    self.wfile.write(res_body)
                    return None
                request_id = domains['request_id']
                if CALLBACK_POST_URL:
                    res_body = bytes(json.dumps({'code': '200'}), 'utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=UTF-8')
                    self.send_header('Content-Length', str(len(res_body)))
                    self.end_headers()
                    self.wfile.write(res_body)
                domain_queries = {}
                for domain in domains['domains']:
                    print('querying ' + domain)
                    domain_query = json.loads(query.query(domain, raw=False))
                    if 'domain_name' in domain_query:
                        domain_name = domain_query['domain_name']
                        if domain_name not in domain_queries:
                            domain_queries[domain_name] = domain_query
                    time.sleep(2)

                # print(domain_queries)
                if CALLBACK_POST_URL:
                    print('callback post data ' + request_id)
                    rsp = requests.post(CALLBACK_POST_URL, json={
                        "request_id": request_id,
                        "result": domain_queries
                    })
                    print(rsp.text)
                    pass
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=UTF-8')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(domain_queries), 'utf-8'))
            except RuntimeError as e:
                print(e)
                if CALLBACK_POST_URL is None:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json; charset=UTF-8')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({'code': '500'}), 'utf-8'))
            pass


Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
