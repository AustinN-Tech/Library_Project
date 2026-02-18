import sqlite3
import logging
# package the code? <-- learn how to do this
from utility_functions import *
from pathlib import Path
from storage import *

# Logging Setup:
log_file = "app_log.log"
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s', 
    filename=log_file, 
    filemode='w', 
    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Logger initialized in app.py.")


conn = sqlite3.connect(":memory:")

c = conn.cursor()

"""
## Database Table:
id - good practice, assigns an integer to each item, increments
title - title of book
author - author of book
genre - genre (category) of book
date_added - time when book was added to db
file_key - filename in server storage, never changed once added
original_filename - user inputted filename, used for display and readability
"""
c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    author TEXT,
    genre TEXT NOT NULL,
    date_added INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    file_key TEXT NOT NULL UNIQUE,
    original_filename TEXT NOT NULL
)
""")

@error_handling
def add_book(title: str, author: str, genre: str, filename: str) -> None:
    file_key = create_book_file() # Creates file and returns file_key for storage
    with conn:
        c.execute("INSERT INTO books (title, author, genre, filename, file_key) VALUES (?, ?, ?)", 
                  (title, author, genre, filename, file_key))
        print(f"{title} added.\n")
        logger.info(f"Added Book: {title}, file_key: {file_key}")

@error_handling
def delete_book(title: str) -> None:
    with conn:
        c.execute("DELETE FROM books WHERE title=(?)", (title,))
        print(f"{title} deleted.\n")
        logger.info(f"Deleted Book from db: {title}")

@error_handling
def update_book(title: str, column: str, value: str) -> None:
    with conn:
        c.execute(f"UPDATE books set {column} = (?) WHERE title = (?)", (value, title))
        logger.info(f"Updated Book '{title}', updated {column} with new value of {value}")

# redo this function
def prompt_update() -> str:
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

def display_all_books() -> list[str]:
    with conn:
        c.execute("SELECT * FROM books")
        results = c.fetchall()

        if results:
            data = [] # create empty list to store results

            for row in results:
                data.append(return_formatted_output(row[1], row[2], row[3], row[4])) # append list with formatted data

            logger.info("Returned All Book Data")
            return data
        else:
            print("No books found.")
            logger.info("No books found in database.")

@error_handling
def get_book(title: str) -> tuple[any] | None:
    with conn:
        c.execute("SELECT * FROM books WHERE title=(?)", (title,))
        row = c.fetchone()
        if not row:
            logger.info(f"get_book(): {title} -> NOT FOUND")
            return
        
        logger.info(f"Returned get_book(): {title}")
        return row

# Make general return function...
def return_file_key(title: str) -> str | None:
    with conn:
        c.execute("SELECT file_key FROM books WHERE title=(?)", (title,))
        row = c.fetchone()
        if not row: # if it returns nothing, return none
            logger.info(f"return_file_key: {title} -> NOT FOUND")
            return None
        
        file_key = row[0] # since it returns a tuple, we must index it
        logger.info(f"return_file_key: {title} -> {file_key}")
        return file_key
    
def return_title(file_key: str) -> str:
    with conn:
        c.execute("SELECT title FROM books where file_key=(?)", (file_key,))
        row = c.fetchone()
        if not row: # if it returns nothing, return none
            logger.info(f"return_title(): {file_key} -> NOT FOUND")
            return None
        
        title = row[0] # since it returns a tuple, we must index it
        logger.info(f"returned title from {file_key}: {title}")
        return file_key

@error_handling
def full_delete(title: str) -> None:
    file_key = return_file_key(title) # obtain file_key
    delete_book(title) # delete from SQL db
    delete_book_file(file_key) # delete filepath (now fully deleted)

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


def main() -> None:
    add_book("Test 1".lower(), "John Doe".lower(), "horror")

    add_book("Test 2".lower(), "Jane Doe".lower(), "adventure")

    terminal_menu()


if __name__ == "__main__":
    main()

conn.commit()
conn.close()