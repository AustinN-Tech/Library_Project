import logging
import sqlite3
from datetime import datetime # for formatting time
from pathlib import Path
import time # for getting current time
import secrets # for random hex characters

genres = ["Fiction", "Non-Fiction", "Fantasy", "Mystery / Thriller", "Sci-Fi",
                 "Historical", "Biography", "Historical", "Science & Technology"]

allowed_columns = {"title": "title","genre": "genre","date_added": "date_added",}

def initialize_logging():
    log_file = "app_log.log"
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s', 
        filename=log_file, 
        filemode='w', 
    level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("Logger initialized in %s.py", __name__)
    return logger

logger = initialize_logging()

def error_handling(func): #error handling logic decorator
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            logger.error(f"Database error occurred in {func.__name__}: {e}") #returns original function name, good for logging
        except Exception as e:
            logger.error(f"Error occurred in {func.__name__}: {e}")
    return wrapper

# Prompts User for Book Title:
@error_handling
def get_title() -> str:
    title = input("Enter title of book: ").strip().lower()
    while not title:
        print("Title cannot be empty. Enter a title.")
        title = input("\nEnter title of book: ").strip().lower()
    return title

# Prompts User for Book Author:
@error_handling
def get_author() -> str:
    author = input("Enter author of book: ").strip().lower()
    if not author: 
        author = "unknown"
    return author

# Prompts User for Book Genre:
@error_handling
def get_genre() -> str:
    print("Select Genre of Book")
    for i, genre in enumerate(genres, start=1):
        print(f" {genre}: [{i}]")

    result = input("Enter Corresponding Number: ").strip()
    while (not result.isdigit()) or (not (1 <= int(result) <= len(genres))):
        print("Invalid Selection. Select a valid genre number.")
        result = input("Enter Corresponding Number: ").strip()
    
    return genres[int(result)-1]

@error_handling
def get_column() -> str:
    column = input("Change Data:\nTitle [1]\nAuthor[2]\nGenre[3]\nEnter Number: ").strip()
    while column not in ["1" ,"2", "3"]:
        print("Invalid Choice. Choose from (1-3)")
        column = input("\nChange Data:\nTitle [1]\nAuthor[2]\nGenre[3]\nEnter Number: ").strip()
    print("\n")
    if column == "1": 
        column = "title"
    elif column == "2":
        column = "author"
    else: 
        column = "genre"
    return column

@error_handling
def get_value() -> str:
    value = input("Enter new value: ").strip().lower()
    while not value:
        print("Value cannot be empty. Enter a value.")
        value = input("\nEnter new value: ").strip().lower()
    return value

@error_handling
def get_OG_filename() -> str:
    filename = input("Enter book filename: ").strip().lower()
    while not filename:
        print("Filename cannot be empty. Enter a filename.")
        filename = input("\nEnter filename of book: ").strip().lower()
    return filename

@error_handling
def get_path() -> Path:
    path = input("Enter book path: ").strip().lower()
    while not path:
        print("Book path cannot be empty. Enter a path.")
        path = input("\nEnter path of book: ").strip().lower()
    path = path.strip().strip('"').strip("'")
    path = Path(path).expanduser() # converts to path datatype
    return path

def get_content() -> str:
    content = input("Enter content of book: ").strip()
    return content

def validate_column(column: str) -> str | None:
    if column.strip().lower() not in allowed_columns:
        logger.debug(f"Incorrect column input {column}")
        return None
    return allowed_columns[column.strip().lower()]

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

def main() -> None:
    pass

if __name__ == "__main__":
    main()