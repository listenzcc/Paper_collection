import os
import webbrowser
from local_toolbox import DataWorker
from local_toolbox import ResquestHandler
from local_toolbox import http_server
from http.server import HTTPServer


# Init host
domain = 'localhost'
port = 8619
host = (domain, port)

# Init data workers
paths = dict(
    pdfdir=os.path.join(os.environ['ONEDRIVE'],
                        'Documents', 'schorlar', 'buffer'),
    raw_df=os.path.join('..', 'paper_jsons', 'raw.json'),
    custom_df=os.path.join('..', 'paper_jsons', 'custom.json')
)
worker = DataWorker(paths, newcustom=False)
server = http_server(worker, host, ResquestHandler)


if __name__ == '__main__':
    url = 'http://{domain}:{port}'.format(domain=domain, port=port)
    webbrowser.open(url)
    server.start()
