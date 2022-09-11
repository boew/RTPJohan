#!/usr/bin/python3.9 
# Based on example from https://docs.python.org/3.9/library/http.server.html 
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
