import sqlite3

_DATABASE_PATH = "./collective_intelligence/searchengine/database/index.db"

db = sqlite3.connect(_DATABASE_PATH)
result = db.execute("select w0.urlid, w0.location, w1.location \
            from wordlocation w0, wordlocation w1\
                where w0.urlid = w1.urlid\
                    and w0.wordid = 1 and w1.wordid = 8").fetchall()
print(result[:100])
