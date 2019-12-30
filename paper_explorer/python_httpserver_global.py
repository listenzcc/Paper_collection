import os
import time
import json
import webbrowser
import urllib.parse
from pprint import pprint
from http.server import HTTPServer, BaseHTTPRequestHandler

data = {'result': 'this is a test'}
domain = 'localhost'
port = 8619
host = (domain, port)


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        # Overwrite do_GET method of BaseHTTPRequestHandler
        # Send 200 response
        # Claim return content-type as json
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Parse url
        # After urlparse, self.query is formated
        self.urlparse()
        if self.query['method'] == 'GET':
            # If method is GET
            # Get content of the file
            # Response content of error message
            error = False
            try:
                content = self.get_file()
            except Exception as e:
                self.wfile.write(json.dumps(self.error_message(repr(e))).encode())
                error = True
            if not error:
                self.wfile.write(json.dumps(content).encode())

    def error_message(self, error_message):
        message = dict(
            url=self.path,
            query=self.query,
            error=error_message
        )
        return message

    def get_file(self):
        file = dict(
            path=self.query['file'],
            format=self.query['file'].split('.')[-1],
            content=''
        )
        file['content'] = json.load(open(file['path'], 'r'))
        if file['format'] == 'json':
            return file['content']
        return file

    def log_messages(self, messages='[None]', end=''):
        # Logger
        print('-' * 80)
        print('[{}]'.format(time.time()))
        if isinstance(messages, str):
            messages = [messages]
        for message in messages:
            pprint(message)
        print(end)

    def urlparse(self):
        # Custom urlparse
        parsed = urllib.parse.urlparse(self.path)
        # Format self.query
        self.query = dict(
            method='GET'  # Default method is GET
        )
        # Parse query in requests
        for query in parsed.query.split('|'):
            # Ignore inlegal query
            if '=' not in query:
                continue
            # Setup query
            a, b = query.split('=', 1)
            self.query[a] = b
        # Log requests
        self.log_messages([parsed, self.query])


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print('Starting server, listen at: {domain}:{port}'.format(
        domain=domain, port=port))
    url = 'http://{domain}:{port}/?|file=../paper_jsons/papers.json|aa=bb'.format(
        domain=domain, port=port)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('keyboard interrupt')
    finally:
        server.server_close()
