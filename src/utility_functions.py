import logging
import sqlite3
import functools
from datetime import datetime # for formatting time
from pathlib import Path
import time # for getting current time
import secrets # for random hex characters

genres = ["Fiction", "Non-Fiction", "Fantasy", "Mystery / Thriller", "Sci-Fi",
                 "Historical", "Biography", "Historical", "Science & Technology"]

allowed_columns = {"title": "title","author":"author","genre": "genre","date_added": "date_added", "bookmark_page":"bookmark_page"}

def initialize_logging(name: str):
    log_file = "app_log.log"
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s', 
        filename=log_file, 
        filemode='w', 
    level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.debug(f"Logger initialized in {name}.py")
    return logger

logger = initialize_logging(__name__)

def error_handling(func): #error handling logic decorator
    @functools.wraps(func) # preveres original function metadata
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            logger.error(f"Database error occurred in {func.__name__}: {e}") #returns original function name, good for logging
            raise
        except Exception as e:
            logger.error(f"Error occurred in {func.__name__}: {e}")
            raise
    return wrapper


@error_handling
def validate_column(column: str) -> str | None:
    if column.strip().lower() not in allowed_columns: # validating column
        logger.debug(f"Incorrect column input {column}")
        return None
    return allowed_columns[column.strip().lower()] # obtaining columns from safe dictionary

@error_handling
def validate_order(order: str) -> str | None:
    order = order.strip().lower()
    if order in ("asc", "ascending"):
        return "ASC"
    elif order in ("desc", "descending"):
        return "DESC"
    logger.debug(f"Invalid order type: {order}")
    return None

# Returns formatted output of book for terminal printing
@error_handling
def return_formatted_output(title, author, genre, date_added) -> str:
    dt = datetime.fromtimestamp(date_added) # formatting time to datetime
    formatted_output = f"Book Title: {title.title()}\nBook Author: {author.title()}\nGenre: {genre.title()}\nDate Added: {dt.strftime('%Y-%m-%d')}"
    return formatted_output

# returns unique filename for db storage
@error_handling
def create_file_key(file_type: str) -> str:
    if file_type not in ["pdf", "txt"]:
        logger.debug(f"Incorrect Filetype: {file_type} passed in create_file_key()")
        return
    current_time = int(time.time()) # obtains current time
    rand = secrets.token_hex(2) # gets 4 random hex characters for guaranteed unique name
    filekey = f"book_{current_time}_{rand}.{file_type}"
    logger.debug(f"Created file_key {filekey}")
    return filekey

# File Checking Functions:
def allowed_book_filename(filename):
    if not filename.lower().endswith(".pdf"):
        return False
    return True

def check_book_magic_bytes(file):
    magic_bytes = file.read(5) # obtain first 5 bytes of file (magic bytes which identify file type)
    file.seek(0) # reset file reader

    if not magic_bytes == b"%PDF-": #checks magic_bytes against bytes of %PDF-
        return False
    return True

def book_file_check(file):
    if file.name == "": return False
    if not allowed_book_filename(file.filename) or not check_book_magic_bytes(file):
        return False
    return True

def cover_file_check(file):
    if file.name == "": return False
    if not allowed_cover_filename(file.filename) or not check_cover_magic_bytes(file):
        return False
    return True

def allowed_cover_filename(filename):
    if not filename.lower().endswith((".png", ".jpg")):
        return False
    return True

def check_cover_magic_bytes(file):
    magic_bytes = file.read(8) # obtain first 8 bytes of file, 8 needed for png
    file.seek(0) # reset file reader

    if magic_bytes.startswith(b"\x89PNG\r\n\x1a\n"): # PNG signature (8 bytes)
        return True
    if magic_bytes.startswith(b"\xff\xd8"):  # JPEG signature
        return True
    return True

def main() -> None:
    pass

if __name__ == "__main__":
    main()