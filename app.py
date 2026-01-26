import sqlite3

conn = sqlite3.connect(":memory:")

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
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Error", e)
    return wrapper

@error_handling
def add_book(title, author):
    with conn:
        c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))

@error_handling
def delete_book():
    pass

@error_handling
def update_book():
    pass

@error_handling
def get_book(title):
    with conn:
        c.execute("SELECT * FROM books WHERE title=(?)", (title,))
        print(c.fetchone())

add_book("Test 2", "Sir Bubbles")
add_book("Test 1", "Sir Bubbles")
get_book("Test 1")


conn.commit()
conn.close()