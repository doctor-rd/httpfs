#!/usr/bin/env python3

from sys import argv
from http.client import HTTPConnection

path = argv[1]
data = ""
if len(argv)>2:
	data = argv[2]
if not path.startswith("/"):
    path = "/"+path
conn = HTTPConnection("localhost:8080")
conn.request("PUT", path, data)
r = conn.getresponse()
print(r.status, r.reason)
