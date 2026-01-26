import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    author TEXT,
    date_added INTEGER NOT NULL DEFAULT (strftime('%s','now'))
)
""")

def error_handling(func):
    def wrapper():
        try:
            func
        except:
            print("Error")
    return wrapper()

@error_handling
def add_book():
    pass

@error_handling
def delete_book():
    pass

@error_handling
def update_book():
    pass

@error_handling
def get_book():
    pass

conn.commit()
conn.close()