import sqlite3
from utility_functions import error_handling, get_author, get_title, get_genre, return_formatted_output


conn = sqlite3.connect(":memory:")

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    author TEXT,
    genre TEXT NOT NULL,
    date_added INTEGER NOT NULL DEFAULT (strftime('%s','now'))
)
""")

@error_handling
def add_book(title, author, genre):
    with conn:
        c.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))
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

    column = input("Change Data:\nTitle [1]\nAuthor[2]\nGenre[3]\nEnter Number: ")
    while column not in ["1" ,"2", "3"]:
        print("Invalid Choice. Choose from (1-3)")
        column = input("\nChange Data:\nTitle [1]\nAuthor[2]\nEnter Number: ")
    print("\n")
    if column == "1": 
        column = "title"
    elif column == "2":
        column = "author"
    else: 
        column = "genre"

    value = input("Enter new value: ").strip().lower()
    while not value: 
        print("Value cannot be empty. Enter a value.")
        value = input("\nEnter new value: ").strip().lower()
    print("\n")

    return title, column, value

def display_all_books():
    with conn:
        c.execute("SELECT * FROM books")
        results = c.fetchall()

        if results:
            data = [] # create empty list to store results

            for row in results:
                data.append(return_formatted_output(row[1], row[2], row[3], row[4])) # append list with formatted data

            return data
        else:
            print("No books found.")

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
        genre = get_genre()
        add_book(title, author, genre)
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

add_book("Test 1".lower(), "John Doe".lower(), "horror")

add_book("Test 2".lower(), "Jane Doe".lower(), "adventure")

terminal_menu()


conn.commit()
conn.close()