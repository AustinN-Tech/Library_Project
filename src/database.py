import sqlite3
# package the code? <-- learn how to do this
from utility_functions import *
from storage import *

logger = initialize_logging() # setting logging

conn = sqlite3.connect("library.db")

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
def add_book(title: str, author: str, genre: str, filename: str, path: Path) -> None:
    file_key = create_book_pdf(path) # Creates file and returns file_key for storage
    with conn:
        c.execute("INSERT INTO books (title, author, genre, original_filename, file_key) VALUES (?, ?, ?, ?, ?)", 
                  (title, author, genre, filename, file_key))
        print(f"{title.title()} added.\n")
        logger.info(f"Added Book: {title}, file_key: {file_key}")

@error_handling
def delete_book(title: str) -> None:
    with conn:
        c.execute("DELETE FROM books WHERE title=(?)", (title,))
        print(f"{title} deleted.\n")
        logger.info(f"Deleted Book from db: {title}")

@error_handling
def delete_all_db() -> None:
    with conn:
        c.execute("DELETE FROM books")
        print("All books deleted.")
        logger.info(f"All rows deleted in library.db")

@error_handling
def full_delete_all_db() -> None:
    with conn:
        c.execute("SELECT * FROM books")
        results = c.fetchall()
        if results:
            for row in results:
                full_delete(title=row[1])
            print("All books fully deleted.")
            logger.info(f"All book files and rows in db deleted from library.")
        else:
            print("No books found.")
            logger.info("No books found in database.")

@error_handling
def update_book(title: str, column: str, value: str) -> None:
    ALLOWED_COLUMNS = {"title", "author", "genre", "original_filename"}
    if column not in ALLOWED_COLUMNS: # check if column input is valid
        raise ValueError("Invalid column")
    with conn:
        c.execute(f"UPDATE books set {column} = (?) WHERE title = (?)", (value, title))
        print(f"Updated {title.capitalize()}'s {column} with new value of {value}")
        logger.info(f"Updated Book '{title}', updated {column} with new value of {value}")

@error_handling
def display_all_books() -> list[str] | None:
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

# Searches using incomplete inputs (ie: title entered "Tale of" returns book titled "Tale of the Turtle")
@error_handling
def partial_search(title: str) -> tuple[any] | None:
        search = f"%{title}%" # format user input with % wildcard
        with conn:
            c.execute("SELECT * FROM books WHERE title LIKE ?", (search,))
            results = c.fetchall()
            if not results:
                logger.info(f"partial_search(): {search} -> NOT FOUND")
                return
            logger.info(f"Returned partial_search(): {search}")
            return results

@error_handling   
def filter(column: str, value: str | None, order: str) -> list[str]:
    data = [] # create empty list to store results

    column = validate_column(column)
    order = validate_order(order)
    if not column or not order: # if column or order invalid, return
        return data # returns empty data

    if value is not None and value != "":
        query = f"SELECT * FROM books WHERE {column} LIKE (?) ORDER BY {column} {order}"
        params = (value,)
        c.execute(query, params)
    else: # if not filtered by direct value
        query = (f"SELECT * FROM books ORDER BY {column} {order}")
        c.execute(query)

    results = c.fetchall()
    for row in results:
        data.append(row) # append list with formatted data
    logger.info("Returned filtered data")
    return data

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
def return_title(file_key: str) -> str | None:
    with conn:
        c.execute("SELECT title FROM books where file_key=(?)", (file_key,))
        row = c.fetchone()
        if not row: # if it returns nothing, return none
            logger.info(f"return_title(): {file_key} -> NOT FOUND")
            return None
        
        title = row[0] # since it returns a tuple, we must index it
        logger.info(f"returned title from {file_key}: {title}")
        return title

@error_handling
def full_delete(title: str) -> None:
    file_key = return_file_key(title) # obtain file_key
    delete_book_file(file_key) # delete filepath (now fully deleted)
    delete_book(title) # delete from SQL db

def main() -> None:
    pass

if __name__ == "__main__":
    main()