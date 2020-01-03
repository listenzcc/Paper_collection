import os
import webbrowser
from local_toolbox import DataWorker
from local_toolbox import ResquestHandler
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


class http_server():
    def __init__(self, worker, host, request_handler_class):
        self.server = HTTPServer(host, request_handler_class)
        self.server.worker = worker
        print('Starting server, listen at: {}:{}'.format(*host))

    def start(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print('Interrupted')
        finally:
            self.server.worker.save_custom()
            self.server.server_close()


server = http_server(worker, host, ResquestHandler)


if __name__ == '__main__':
    url = 'http://{domain}:{port}'.format(domain=domain, port=port)
    webbrowser.open(url)
    server.start()
