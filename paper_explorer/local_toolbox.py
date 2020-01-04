import os
import json
import time
import urllib.parse
import pandas as pd
from pprint import pprint
from http.server import HTTPServer, BaseHTTPRequestHandler


class DataWorker():
    def __init__(self, paths, newcustom=False):
        # Init path and df
        # pdfdir: dir path of pdf files
        # custom_df: custom df
        # raw_df: raw df
        self.paths = paths
        self.pdfdir = paths.get('pdfdir')
        self.raw_df = pd.read_json(paths.get('raw_df'))
        if newcustom:
            self.custom_df = pd.DataFrame()
        else:
            self.custom_df = pd.read_json(paths.get('custom_df'))

    def update_custom(self, query, datas):
        # Update custom df as query
        uid = query.get('uid', 'uid')
        # New Series
        se = pd.Series(datas, name=uid)
        # # Inject items as datas
        # for key in datas:
        #     se[key] = datas[key]
        # Override uid row of custom_df
        self.custom_df.drop(index=uid, inplace=True, errors='ignore')
        self.custom_df = self.custom_df.append(se)
        # Replace NaN into ''
        self.custom_df[self.custom_df.isna()] = ''
        print(self.custom_df)

    def save_custom(self):
        print(self.custom_df)
        print('Saving custom as {}'.format(self.paths.get('custom_df')))
        self.custom_df.to_json(self.paths.get('custom_df'))

    def get_pdf(self, fname):
        # Get pdf from pdfdir
        # fname: fname of pdf file
        # Replace %20 into [space]
        fname = fname
        fullpath = os.path.join(self.pdfdir, fname)

        # Check if file exists
        # Return if not
        if not os.path.exists(fullpath):
            raise FileNotFoundError(fullpath)

        # Read pdf file and return as bytes
        with open(fullpath, 'rb') as fp:
            pdf_bits_list = fp.readlines()
        return b''.join(pdf_bits_list)


class ResquestHandler(BaseHTTPRequestHandler):
    def send_response_content(self, content_type, content, allow_origin_access=True):
        # Response 200
        self.send_response(200)
        # Allow origin access
        if allow_origin_access:
            self.send_header('Access-Control-Allow-Origin', '*')
        # Send correct header
        self.send_header('Content-Type', 'application/{}'.format(content_type))
        self.end_headers()
        # Send content
        self.wfile.write(content)

    def send_default_json(self):
        # Hello there
        self.send_response_content('json', json.dumps([
            'Hello there.',
            '?get=raw: get raw_df.json',
            '?get=custom: get custom_df.json',
            '?get=pdf&fname=fname: get pdf file of filename',
            '?set=custom&uid=[xx]: set custom_df.json, note that you should use POST method to provide data'
        ]).encode())

    def do_POST(self):
        # Overwrite do_POST method of BaseHTTPRequestHandler
        # Parse request first
        self.urlparse()
        # Parse data
        datas = self.dataparse(self.rfile.read(int(self.headers['content-length'])))
        # Link data worker
        worker = self.server.worker
        worker.update_custom(self.query, datas)
        # Send default json
        self.send_default_json()

    def do_GET(self):
        # Overwrite do_GET method of BaseHTTPRequestHandler
        # Parse request first
        self.urlparse()
        # Link data worker
        worker = self.server.worker

        # Get raw_df
        if self.query.get('get', '') == 'raw':
            self.send_response_content(
                'json', worker.raw_df.to_json(orient='records').encode())
            return

        # Get custom_df
        if self.query.get('get', '') == 'custom':
            self.send_response_content(
                'json', worker.custom_df.to_json().encode())
            return

        # Get PDF file
        if self.query.get('get', '') == 'pdf':
            self.send_response_content(
                'pdf', worker.get_pdf(self.query.get('fname', '')))
            return

        # Update custom_df
        # if self.query.get('set', '') == 'custom':
        #     worker.update_custom(self.query)
        #     self.send_response_content(
        #         'json', worker.custom_df.to_json().encode())
        #     return

        # Hello there
        self.send_default_json()

    def error_message(self, error_message):
        # Log error_message
        message = dict(
            url=self.path,
            query=self.query,
            error=error_message
        )
        self.log_messages(message, end='!!!!!!!Error Error Error!!!!!!')
        return message

    def log_messages(self, messages='[None]', end=''):
        # Logger
        print('-' * 80)
        print('[{}]'.format(time.time()))
        pprint(messages)
        print(end)

    def dataparse(self, data):
        # Parse data from post request
        # data: data from post request
        data = urllib.parse.unquote(data.decode())
        datas = dict()
        for e in data.split('&'):
            if not '=' in e:
                continue
            a, b = e.split('=', 1)
            datas[a] = b
        self.log_messages(datas)
        return datas

    def urlparse(self):
        # Custom urlparse
        # unquote: unquote HTML content
        # urlparse: parse unquoted path
        parsed = urllib.parse.urlparse(urllib.parse.unquote(self.path))
        # Format self.query
        self.query = dict()
        # Parse query in requests
        for query in parsed.query.split('&'):
            # Ignore inlegal query
            if '=' not in query:
                continue
            # Setup query
            a, b = query.split('=', 1)
            # Fix known convertion issue
            self.query[a] = b  # .replace('%20', ' ')
        # Log requests
        self.log_messages([parsed, self.query])
