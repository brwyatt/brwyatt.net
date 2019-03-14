#!/usr/bin/env python3

# Largely based on code by Integralist on GitHub:
# https://gist.github.com/Integralist/ce5ebb37390ab0ae56c9e6e80128fdc2

from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import os
from random import randint
import re
import time
from urllib.parse import urlparse, parse_qs

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 8000)
HOST_PORT = f'{HOST}:{PORT}'
LATENCY = int(os.environ.get('LATENCY', 0))
LATENCY_JITTER = int(os.environ.get('LATENCY_JITTER', LATENCY*0.25))

os.environ['LOGLEVEL'] = 'DEBUG'
os.environ['STAGE'] = 'Alpha'
os.environ['WEB_DOMAIN'] = HOST_PORT
os.environ['API_DOMAIN'] = HOST_PORT


def load_handlers(routes):
    route_handlers = []

    for route, file_path in routes:
        spec = importlib.util.spec_from_file_location("name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        route_handlers.append((route, module.handler))

    return route_handlers


routes = load_handlers([
    (r'^/$', 'lambda/web/page_renderer.py'),
    (r'^/css/(?P<resource>.*)$', 'lambda/web/fetch_static.py'),
    (r'^/js/(?P<resource>.*)$', 'lambda/web/fetch_static.py'),
    (r'^/pages/content$', 'lambda/api/get_pagecontent.py'),
    (r'^/(?P<proxy>.*)$', 'lambda/web/page_renderer.py'),
])


class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        queryParams = {x: y[0] for x, y in
                       parse_qs(urlparse(self.path).query).items()}
        for route, handler in routes:
            match = re.match(route, path)
            if match:
                event = {
                    'path': path,
                    'pathParameters': match.groupdict(),
                    'queryStringParameters': queryParams,
                    'requestContext': {
                        'identity': {
                            'sourceIp': '127.0.0.1',
                        },
                    },
                    'resource': path,  # close enough
                    'stageVariables': {
                        'HostName': HOST_PORT,
                    }
                }
                res = handler(event, None)

                if LATENCY:
                    time.sleep(LATENCY + randint(
                        -LATENCY_JITTER, LATENCY_JITTER))

                self.send_response(int(res['statusCode']))
                for header, value in res.get('headers', {}).items():
                    self.send_header(header, value)
                if 'Content-Type' not in res.get('headers', {}):
                    self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                if type(res['body']) is str:
                    self.wfile.write(bytes(res['body'], 'UTF-8'))
                elif type(res['body']) is bytes:
                    self.wfile.write(res['body'])
                else:
                    raise Exception(
                        'Cannot write type "{type(res["body"])}" to client!')
                return


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST, PORT), RequestHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST, PORT))
