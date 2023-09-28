import sqlite3

DBNAME = 'shichigo.db'

conx = sqlite3.connect(DBNAME)
cur = conx.cursor()

cur.execute(
  'CREATE TABLE shichigo(\
    id      INTEGER   PRIMARY KEY AUTOINCREMENT,\
    poem    TEXT      NOT NULL,\
    writer  TEXT      NOT NULL,\
    fav     INTEGER   DEFAULT 0,\
    replies TEXT,\
    ts                DEFAULT CURRENT_TIMESTAMP\
  )'
)

conx.commit()
conx.close()