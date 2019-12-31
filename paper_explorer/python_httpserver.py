import os
import time
import json
import webbrowser
import urllib.parse
import pandas as pd
from pprint import pprint
from http.server import HTTPServer, BaseHTTPRequestHandler

domain = 'localhost'
port = 8619
host = (domain, port)

raw_df = pd.read_json(os.path.join('..', 'paper_jsons', 'raw.json'))
custom_df = pd.read_json(os.path.join('..', 'paper_jsons', 'custom.json'))


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        # Overwrite do_GET method of BaseHTTPRequestHandler
        # Send 200 response
        # Claim return content-type as json
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.urlparse()
        # Get raw_df
        if self.query.get('get', '') == 'raw':
            self.wfile.write(raw_df.to_json(orient='records').encode())
            return
        # Get custom_df
        if self.query.get('get', '') == 'custom':
            self.wfile.write(custom_df.to_json(orient='records').encode())
            return
        # Hello there
        self.wfile.write(json.dumps([
            'Hello there.',
            '?get=raw: get raw_df.json',
            '?get=custom: get custom_df.json'
            ]).encode())

    def error_message(self, error_message):
        message = dict(
            url=self.path,
            query=self.query,
            error=error_message
        )
        return message

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
        self.query = dict()
        # Parse query in requests
        for query in parsed.query.split(','):
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
    url = 'http://{domain}:{port}'.format(
        domain=domain, port=port)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('keyboard interrupt')
    finally:
        server.server_close()
