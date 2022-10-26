#!/usr/bin/env python3

from sys import argv
from http.client import HTTPConnection

path = argv[1]
if not path.startswith("/"):
    path = "/"+path
conn = HTTPConnection("localhost:8080")
conn.request("DELETE", path)
r = conn.getresponse()
print(r.status, r.reason)
