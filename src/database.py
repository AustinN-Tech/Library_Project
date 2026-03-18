import sqlite3
from dataclasses import dataclass
# package the code? <-- learn how to do this
from utility_functions import *
from storage import *

logger = initialize_logging() # setting logging

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

# c.execute("""
# CREATE TABLE IF NOT EXISTS books (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT UNIQUE NOT NULL,
#     author TEXT NOT NULL DEFAULT 'Unknown',
#     genre TEXT NOT NULL,
#     date_added INTEGER NOT NULL DEFAULT (strftime('%s','now')),
#     file_key TEXT NOT NULL UNIQUE,
#     cover_path TEXT NOT NULL,
#     original_filename TEXT NOT NULL
# )
# """)

@dataclass
class Book:
    id: int
    title: str
    genre: str
    date_added: int
    file_key: str
    cover_path: str
    original_filename: str
    author: str = 'Unknown'

def row_to_book(row) -> Book:
    return Book(
        id = row[0],
        title = row[1],
        author = row[2],
        genre = row[3],
        date_added = row[4],
        file_key = row[5],
        cover_path = row[6],
        original_filename= row[7]
    )

# work in progress function
def db_connection_handling(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("library.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def open_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect("library.db")
    return conn, conn.cursor()

@error_handling
def add_book(title: str, author: str, genre: str, filename: str, path: Path) -> None:
    conn, c = open_connection() # open connection to db

    file_key = create_book_pdf(path)
    cover_path = generate_cover(return_pdf_file_path(file_key), file_key)
    try:
        with conn:
            c.execute("INSERT INTO books (title, author, genre, original_filename, file_key, cover_path) VALUES (?, ?, ?, ?, ?, ?)", 
                    (title, author, genre, filename, file_key, cover_path))
            print(f"{title} added.\n")
            logger.info(f"Added Book: {title}, file_key: {file_key}")
    finally:
        conn.close()

@error_handling
def delete_book(book: Book) -> None:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("DELETE FROM books WHERE id=(?)", (book.id,))
            print(f"{book.title} deleted.\n")
            logger.info(f"Deleted Book from db: {book.title}")
    finally:
        conn.close()

@error_handling
def delete_all_db() -> None:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("DELETE FROM books")
            print("All books deleted.")
            logger.info(f"All rows deleted in library.db")
    finally:
        conn.close()

@error_handling
def full_delete_all_db() -> None:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("SELECT * FROM books")
            results = c.fetchall()
            if results:
                for row in results:
                    book = row_to_book(row)
                    full_delete(book)
                print("All books fully deleted.")
                logger.info(f"All book files and rows in db deleted from library.")
            else:
                print("No books found.")
                logger.info("No books found in database.")
    finally:
        conn.close()
    
@error_handling
def update_book(book: Book, column: str, value: str) -> None:
    ALLOWED_COLUMNS = {"title", "author", "genre", "original_filename"}
    if column not in ALLOWED_COLUMNS: # check if column input is valid
        raise ValueError("Invalid column")
    
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute(f"UPDATE books set {column} = (?) WHERE id = (?)", (value, book.id))
            print(f"Updated {book.title.capitalize()}'s {column} with new value of {value}")
            logger.info(f"Updated Book '{book.title}', updated {column} with new value of {value}")
    finally:
        conn.close()

@error_handling
def return_all_books() -> list[Book]:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("SELECT * FROM books")
            results = c.fetchall()
            if results:
                data = [] # create empty list to store results
                for row in results:
                    book = row_to_book(row) # using book object (much more readable)
                    data.append(book) # append list with book object
                logger.info("Returned All Book Data")
                return data
            else:
                print("No books found.")
                logger.info("No books found in database.")
    finally:
        conn.close()

@error_handling
def get_book_by_title(title: str) -> Book | None:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("SELECT * FROM books WHERE title=(?)", (title,))
            row = c.fetchone()
            if not row:
                logger.info(f"get_book_by_title(): {title} -> NOT FOUND")
                return
            logger.info(f"Returned get_book_by_title(): {title}")
            return row_to_book(row) # convert row to book object
    finally:
        conn.close()
    
@error_handling
def get_book_by_id(book_id: int) -> Book | None:
    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("SELECT * FROM books WHERE id=(?)", (book_id,))
            row = c.fetchone()
            if not row:
                logger.info(f"get_book_by_id(): {book_id} -> NOT FOUND")
                return
            logger.info(f"Returned get_book_by_id(): {book_id}")
            return row_to_book(row) # convert row to book object
    finally:
        conn.close()

# Searches using incomplete inputs (ie: title entered "Tale of" returns book titled "Tale of the Turtle")
@error_handling
def partial_search(title: str) -> list[Book]:
    search_results = []
    search = f"%{title}%" # format user input with % wildcard

    conn, c = open_connection() # open connection to db

    try:
        with conn:
            c.execute("SELECT * FROM books WHERE title LIKE ?", (search,))
            database_results = c.fetchall()

            if not database_results:
                logger.info(f"partial_search(): {search} -> NOT FOUND")
                return search_results # would be empty list
            
            for row in database_results:
                book = row_to_book(row) # convert row to book object
                search_results.append(book)
                
            logger.info(f"Returned partial_search(): {search}")
            return search_results
    finally:
        conn.close()

@error_handling   
def filter(column: str, value: str | None, order: str) -> list[Book]:
    search_results = [] # create empty list to store results

    column = validate_column(column)
    order = validate_order(order)
    if not column or not order: # if column or order invalid, return
        return search_results # returns empty data
    
    conn, c = open_connection() # open connection to db

    try:
        if value is not None and value != "":
            query = f"SELECT * FROM books WHERE {column} LIKE (?) ORDER BY {column} {order}"
            params = (f"%{value}%",) # wrap in wildcard so LIKE will enact partial search
            c.execute(query, params)
        else: # if not filtered by direct value
            query = (f"SELECT * FROM books ORDER BY {column} {order}")
            c.execute(query)

        results = c.fetchall()
        for row in results:
            book = row_to_book(row) # converting row to book object
            search_results.append(book) # append list with formatted data
        logger.info("Returned filtered data")
        return search_results
    finally:
        conn.close()

@error_handling
def full_delete(book: Book) -> None:
    delete_book_file(book.file_key) # delete filepath (now fully deleted)
    delete_book_cover(book.cover_path) # delete cover file
    delete_book(book) # delete from SQL db

def main() -> None:
    pass

if __name__ == "__main__":
    main()