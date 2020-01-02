import os
import time
import json
import hashlib
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

class DataWorker():
    def __init__(self):
        # Init path and df
        # pdfpath: path of pdf files
        # custom_df: custom df
        # raw_df: raw df
        self.pdfpath = 'C:\\Users\\liste\\OneDrive\\Documents\\schorlar\\buffer'
        self.raw_df = pd.read_json(os.path.join('..', 'paper_jsons', 'raw.json'))
        self.custom_df = pd.read_json(os.path.join('..', 'paper_jsons', 'custom.json'))

    def update_custom(self, query):
        # Update custom df as query
        uid = query.get('uid', 'uid')
        # New Series
        se = pd.Series(name=uid)
        # Inject items as query
        for key in query:
            if key in ['uid', 'rawpath', 'set']:
                continue
            se[key] = query[key]
        # Override uid row of custom_df
        self.custom_df.drop(index=uid, inplace=True, errors='ignore')
        self.custom_df = self.custom_df.append(se)
        # Replace NaN into '--'
        self.custom_df[self.custom_df.isna()] = ''
        print(self.custom_df)
    
    def get_pdf(self, fname):
        # Get pdf from pdfpath
        # fname: fname of pdf file
        # Replace %20 into [space]
        fname = fname
        fullpath = os.path.join(self.pdfpath, fname)

        # Check if file exists
        # Return if not
        if not os.path.exists(fullpath):
            raise FileNotFoundError(fullpath)

        # Read pdf file and return as bytes
        with open(fullpath, 'rb') as fp:
            pdf_bits_list = fp.readlines()
        return b''.join(pdf_bits_list)

# Init worker
worker = DataWorker()

class Resquest(BaseHTTPRequestHandler):

    def do_GET(self):
        # Overwrite do_GET method of BaseHTTPRequestHandler
        # Send 200 response
        # Claim return content-type as json
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.urlparse()

        # Get raw_df
        if self.query.get('get', '') == 'raw':
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(worker.raw_df.to_json(orient='records').encode())
            return

        # Get custom_df
        if self.query.get('get', '') == 'custom':
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(worker.custom_df.to_json().encode())
            return

        # Get PDF file
        if self.query.get('get', '') == 'pdf':
            self.send_header('Content-type', 'application/pdf')
            self.end_headers()
            self.wfile.write(worker.get_pdf(self.query.get('fname', '')))
            return

        # Update custom_df
        if self.query.get('set', '') == 'custom':
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            worker.update_custom(self.query)
            self.wfile.write(worker.custom_df.to_json().encode())
            return

        # Hello there
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps([
            'Hello there.',
            '?get=raw: get raw_df.json',
            '?get=custom: get custom_df.json',
            '?get=pdf, fname=fname: get pdf file of filename',
            '?set=custom, uid=[], rawpath=[]: set custom_df.json as uid and rawpath'
        ]).encode())

    def error_message(self, error_message):
        message = dict(
            url=self.path,
            query=self.query,
            error=error_message
        )
        self.log_messages(message)
        return message

    def log_messages(self, messages='[None]', end=''):
        # Logger
        print('-' * 80)
        print('[{}]'.format(time.time()))
        pprint(messages)
        print(end)

    def urlparse(self):
        # Custom urlparse
        parsed = urllib.parse.urlparse(self.path)
        # Format self.query
        self.query = dict()
        # Parse query in requests
        for query in parsed.query.split('&'):
            # Ignore inlegal query
            if '=' not in query:
                continue
            # Setup query
            a, b = query.split('=', 1)
            self.query[a] = b.replace('%20', ' ')
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
