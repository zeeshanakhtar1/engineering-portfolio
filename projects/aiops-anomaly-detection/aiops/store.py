"""SQLite-backed retention and query for local infrastructure samples."""
import sqlite3
import time
from pathlib import Path

class MetricStore:
    def __init__(self,path=':memory:'):
        if path!=':memory:':
            Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY, metric TEXT NOT NULL, value REAL NOT NULL, observed_at REAL NOT NULL)')
        self.db.execute('CREATE INDEX IF NOT EXISTS samples_metric_id ON samples(metric,id)')
        self.db.commit()
    def recent(self,metric,limit=100):
        if not 1<=limit<=10000:
            raise ValueError('limit out of range')
        rows=self.db.execute('SELECT value FROM samples WHERE metric=? ORDER BY id DESC LIMIT ?',(metric,limit)).fetchall()
        return [row[0] for row in reversed(rows)]
    def add(self,metric,value):
        if not metric or len(metric)>100:
            raise ValueError('invalid metric')
        with self.db:
            self.db.execute('INSERT INTO samples (metric,value,observed_at) VALUES (?,?,?)',(metric,float(value),time.time()))
    def close(self):
        self.db.close()
