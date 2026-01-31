import sqlite3
from datetime import datetime


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
    title = get_title()
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


def get_title():
    title = input("Enter title of book: ").strip().lower()
    while not title:
        print("Title cannot be empty. Enter a title.")
        title = input("\nEnter title of book: ").strip().lower()

    return title

def get_author():
    author = input("Enter author of book: ").strip().lower()
    if not author: 
        author = "unknown"

    return author

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
    dt = datetime.fromtimestamp(date_added) # formatting time to datetime
    formatted_output = f"Book Title: {title}\nBook Author: {author}\nDate Added: {dt.strftime('%Y-%m-%d')}"
    return formatted_output

@error_handling
def get_book(title):
    with conn:
        c.execute("SELECT * FROM books WHERE title=(?)", (title,))
        return c.fetchone()

def terminal_menu():
    print("\n-====+ Library Database Menu +====-\n")
    print("Add Book [1]\nDelete Book [2]\nUpdate Book [3]\nSearch for Book [4]\nDisplay all Books [5]\nExit [0]")
    result = int(input("Enter corresponding number: "))
    print("\n")
    if result == 1:
        print("-== Add a new Book ==-")
        title = get_title()
        author = get_author()
        add_book(title, author)
        terminal_menu()
    elif result == 2:
        print("-== Delete a Book ==-")
        title = get_title()
        if not get_book(title):
            print(f"No book found with name {title}")
            terminal_menu()
        delete_book(title)
        terminal_menu()
    elif result == 3:
        title, column, value = prompt_update()
        update_book(title, column, value)
        terminal_menu()
    elif result == 4:
        print("-== Search for a Book ==-\n")
        title = get_title()
        retrieved_book = get_book(title)
        if not retrieved_book:
            print(f"No book found with title {title}")
            terminal_menu()
        print(return_formatted_output(retrieved_book))
        terminal_menu()
    elif result == 5:
        print("-== All Books ==-\n")
        data = display_all_books()
        for i in data:
            print(i, "\n")
        terminal_menu()
    elif result == 0:
        print("Exiting...\n")
        return
    else:
        print("Please enter a valid number.")

add_book("Test 1".lower(), "John Doe".lower())

add_book("Test 2".lower(), "Jane Doe".lower())

terminal_menu()


conn.commit()
conn.close()