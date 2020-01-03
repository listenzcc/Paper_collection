import os
import json
import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler


class DataWorker():
    def __init__(self, paths):
        # Init path and df
        # pdfdir: dir path of pdf files
        # custom_df: custom df
        # raw_df: raw df
        self.paths = paths
        self.pdfdir = paths.get('pdfdir')
        self.raw_df = pd.read_json(paths.get('raw_df'))
        self.custom_df = pd.read_json(paths.get('custom_df'))

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
