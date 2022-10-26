import sqlite3

class St:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.cursor().execute('CREATE TABLE IF NOT EXISTS stor (path TEXT UNIQUE, data)')

    def get(self, path):
        c=self.conn.cursor()
        c.execute('SELECT data FROM stor WHERE path=?', (path,))
        r=c.fetchone()
        if r==None:
            raise Exception(404)
        else:
            data = r[0]
            if data==None:
                raise Exception(410)
            else:
                return r[0]

    def put(self, path, data):
        c=self.conn.cursor()
        c.execute('SELECT data FROM stor WHERE path=? AND data=?', (path, data,))
        if c.fetchone()==None:
            c.execute('INSERT OR REPLACE INTO stor VALUES(?,?)', (path, data,))
            self.conn.commit()
            return 201
        else:
            return 204

    def delete(self, path):
        c=self.conn.cursor()
        c.execute('UPDATE stor SET data=NULL WHERE path=?', (path,))
        self.conn.commit()
        return 204
