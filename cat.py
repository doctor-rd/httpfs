#!/usr/bin/env python3

from sys import argv
from http.client import HTTPConnection

path = argv[1]
if not path.startswith("/"):
    path = "/"+path
conn = HTTPConnection("localhost:8080")
conn.request("GET", path)
r = conn.getresponse()
if r.status == 200:
    data = r.read()
    print(data.decode('utf-8'))
else:
    print(r.status, r.reason)
