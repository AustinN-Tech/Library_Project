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
            print("Error: ", e)
    return wrapper

@error_handling
def add_book(title, author):
    with conn:
        c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        print(f"{title} added.\n")

@error_handling
def delete_book(title):
    with conn:
        c.execute("DELETE FROM books WHERE title=(?)", (title,))
        print(f"{title} deleted.\n")

@error_handling
def update_book(title, column, value):
    with conn:
        c.execute(f"UPDATE books set {column} = (?) WHERE title = (?)", (value, title))

def prompt_update():
    title = input("Enter title of book to update: ").strip().lower()
    while not title:        
        print("Title cannot be empty. Enter a title.")
        title = input("\nEnter title of book to update: ").strip().lower()
    print("\n")

    column = input("Change Data:\nTitle [1]\nAuthor[2]\nEnter Number: ")
    while column not in ["1" ,"2"]:
        print("Invalid Choice. Choose from (1-2)")
        column = input("\nChange Data:\nTitle [1]\nAuthor[2]\nEnter Number: ")
    print("\n")
    if column == "1": 
        column = "title"
    else: 
        column = "author"

    value = input("Enter new value: ").strip().lower()
    while not value: 
        print("Value cannot be empty. Enter a value.")
        value = input("\nEnter new value: ").strip().lower()
    print("\n")

    return title, column, value

@error_handling
def get_book(title):
    with conn:
        c.execute("SELECT * FROM books WHERE title=(?)", (title,))
        print(c.fetchone())

add_book("Test 1".lower(), "John Doe".lower())

title, column, value = prompt_update()
update_book(title, column, value)

add_book("Test 2", "Jane Doe")
get_book("Test 3".lower())


conn.commit()
conn.close()