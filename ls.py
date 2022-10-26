#!/usr/bin/env python3

import json
from http.client import HTTPConnection

conn = HTTPConnection("localhost:8080")
conn.request("GET", "/ls.json")
r = conn.getresponse()
if r.status == 200:
    data = r.read()
    lst = json.loads(data.decode('utf-8'))
    for i in lst:
        if i["op"] == "PUT":
            print(i["path"])
else:
    print(r.status, r.reason)
