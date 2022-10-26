#!/usr/bin/env python3

from http.client import HTTPConnection
from db import St
import tarfile

stor = St("stor_copy.db")
c = stor.conn.cursor()
count = 0
c.execute('CREATE TABLE IF NOT EXISTS meta (name TEXT UNIQUE, value)')
c.execute('SELECT value FROM meta WHERE name="count"')
r = c.fetchone()
if r:
    count = r[0]

conn = HTTPConnection("localhost:8080")
conn.request("GET", "/all"+str(count)+".tar.gz")
r = conn.getresponse()
if r.status == 200:
    f = tarfile.open(mode = "r:gz", fileobj = r)
    while True:
        tf = f.next()
        if tf == None:
            break
        if tf.mtime > count:
            count = tf.mtime
        if tf.ischr():
            stor.delete(tf.name)
        else:
            stor.put(tf.name, f.extractfile(tf).read())
    c.execute('INSERT OR REPLACE INTO meta VALUES("count", ?)', (count,))
    stor.conn.commit()
else:
    print(r.status, r.reason)
