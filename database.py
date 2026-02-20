import sqlite3
# package the code? <-- learn how to do this
from utility_functions import *
from pathlib import Path
from storage import *

logger = initialize_logging() # setting logging


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

@error_handling
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
@error_handling
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

@error_handling
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
    delete_book_file(file_key) # delete filepath (now fully deleted)
    delete_book(title) # delete from SQL db

def main() -> None:
    pass

if __name__ == "__main__":
    main()

conn.commit()
conn.close()