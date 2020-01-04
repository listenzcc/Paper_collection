import time
import json
import urllib.parse
from pprint import pprint
from http.server import HTTPServer, BaseHTTPRequestHandler

domain = 'localhost'
port = 8619
host = (domain, port)

class ResquestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('-' * 80)
        print(self.path)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        print('-' * 80)
        print(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        print(datas)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content', 'application/text')
        self.end_headers()
        x = urllib.parse.unquote(datas.decode())
        print(x)
        self.wfile.write(x.encode())

server = HTTPServer(host, ResquestHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Interrupted')
finally:
    server.server_close()