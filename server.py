#!/usr/bin/env python3
"""
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from db import St
import json
import tarfile
from io import BytesIO
import re

class S(BaseHTTPRequestHandler):
    def _set_response(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        c = stor.conn.cursor()
        lst = re.fullmatch('/ls([0-9]*)\.json', self.path)
        tar = re.fullmatch('/all([0-9]*)\.tar\.gz', self.path)
        if self.path == "/":
            self._set_response()
            q = c.execute('SELECT ROWID, path, data IS NULL FROM stor')
            self.wfile.write(b'<table border=1>')
            for i in q:
                self.wfile.write(("<tr><td>"+str(i[0])+"</td><td>").encode('utf-8'))
                if i[2]==1:
                    self.wfile.write(i[1].encode('utf-8'))
                else:
                    self.wfile.write(("<a href="+i[1]+">"+i[1]+"</a>").encode('utf-8'))
                self.wfile.write("</td></tr>".encode('utf-8'))
            self.wfile.write(b'<table>')
        elif lst:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            start = lst.group(1)
            if start:
                q = c.execute('SELECT ROWID, path, data IS NULL FROM stor WHERE ROWID>=?',(start,))
            else:
                q = c.execute('SELECT ROWID, path, data IS NULL FROM stor')
            self.wfile.write(json.dumps([{"count": i[0], "path": i[1], "op": ("DELETE" if i[2]==1 else "PUT")} for i in q]).encode('utf-8'))
        elif tar:
            self.send_response(200)
            self.send_header('Content-type', 'application/tar+gzip')
            self.end_headers()
            start = tar.group(1)
            if start:
                q = c.execute('SELECT ROWID, path, data IS NULL FROM stor WHERE ROWID>=?',(start,))
            else:
                q = c.execute('SELECT ROWID, path, data IS NULL FROM stor')
            f=tarfile.open(mode = "w:gz", fileobj = self.wfile)
            for i in q:
                tf = tarfile.TarInfo(i[1])
                tf.mtime = i[0]
                if i[2]==1:
                    if start:
                        tf.type = tarfile.CHRTYPE
                        f.addfile(tf)
                else:
                    data = stor.get(i[1])
                    tf.size = len(data)
                    f.addfile(tf, BytesIO(data))
            f.close()
        else:
            try:
                res = stor.get(self.path)
                self._set_response()
                self.wfile.write(res)
            except Exception as e:
                self._set_response(e.args[0])

    def do_PUT(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        put_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("PUT request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), put_data.decode('utf-8'))
        self._set_response(stor.put(self.path, put_data))

    def do_DELETE(self):
        logging.info("DELETE request,\nPath: %s\nHeaders:\n%s\n\n",
                str(self.path), str(self.headers))
        self._set_response(stor.delete(self.path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()

def run(server_class=HTTPServer, handler_class=S, port=8080, db='stor.db'):
    global stor
    stor = St(db)
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
