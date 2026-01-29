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
    print("-== Updating Book ==-\n")
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

def prompt_add_book():
  print("-== Adding New Book ==-\n")
  title = input("Enter title of book: ").strip().lower()
  while not title:
    print("Title cannot be empty. Enter a title.")
    title = input("\nEnter title of book: ").strip().lower()
  print("\n")

  author = input("Enter author of book: ")
  if not author:
    author = "Unknown"
  print("\n")

  return title, author

def display_all_books():
    with conn:
        c.execute("SELECT * FROM books")
        results = c.fetchall()

        if results:
            data = [] # create empty list to store results

            for row in results:
                data.append(return_formatted_output(row[1], row[2], row[3])) # append list with formatted data

            return data
        else:
            print("No books found.")


def return_formatted_output(title, author, date_added):
    formatted_output = f"Book Title: {title}\nBook Author: {author}\nDate Added: {date_added}"
    return formatted_output

@error_handling
def get_book(title):
    with conn:
        c.execute("SELECT * FROM books WHERE title=(?)", (title,))
        return c.fetchone()
        #if (c.fetchone()): # if result found, print result
        #    print(c.fetchone())
        #else: # no result, print not found
        #    print(f"No book found with title {title}.")

add_book("Test 1", "John Doe")

add_book("Test 2", "Jane Doe")

data = display_all_books()
for i in data:
  print(i, "\n")




conn.commit()
conn.close()