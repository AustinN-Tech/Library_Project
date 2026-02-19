import logging
from pathlib import Path
from utility_functions import create_file_key, error_handling, initialize_logging

BASE_DIR = Path(__file__).resolve().parent # takes the absolute path of the parent folder of code file
BOOK_DIR = BASE_DIR / "book_pdfs"

logger = initialize_logging() # setting logging

@error_handling
def create_book_directory() -> None:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directory Created {get_directory(BOOK_DIR)}")

@error_handling
def return_file_path(file_key: str) -> Path:
    if Path(file_key).name != file_key:
        raise ValueError(f"Attempted file_key: {file_key} is incorrect. file_key must be a filename only")
    path = BOOK_DIR / file_key
    logger.debug(f"Returned Path {file_key} -> {path}")
    return path

@error_handling
def create_book_file() -> str:
    create_book_directory() # makes a directory is there isn't one
    file_key = create_file_key() # makes unique file_key
    path = return_file_path(file_key)
    path.touch(exist_ok=False) # creates file

    logger.debug(f"File {file_key} created at {path}")
    return file_key

@error_handling
def delete_book_file(file_key: str) -> None:
    path = return_file_path(file_key)
    if path.exists():
        path.unlink()
        logger.debug(f"File {file_key} at {path} fully deleted")
    else:
        raise FileNotFoundError(f"File {file_key} cannot be found.")

@error_handling
def rename_file_key(old_file_key: str, new_file_key: str) -> Path:
    old_path = return_file_path(old_file_key)
    new_path = return_file_path(new_file_key)
    if not old_path.exists(): # if old path not found, raise error
       raise FileNotFoundError(f" Path {old_path} cannot be found.") 
    logger.debug(f"{old_file_key} renamed to {new_file_key} successfully")
    return old_path.rename(new_path)

def get_directory(Directory) -> Path:
    return Path(Directory).resolve()

@error_handling
def write_file(file_key: str, content: str) -> None:
    path = return_file_path(file_key)

    logger.debug(f'Attempting write to file path: {path}...')
    path.write_text(content, encoding="utf-8")
    logger.debug(f'Successfully written to file path: {path}')

@error_handling
def read_file(file_key: str) -> str:
    path = return_file_path(file_key)

    logger.debug(f'Attempting to retrieve content from file path: {path}...')
    text = path.read_text(encoding="utf-8")
    logger.debug(f'Returning content from file path: {path}')
    return text

@error_handling
def file_return(file_key: str) -> Path | None:
    path = return_file_path(file_key)
    if (path.glob(file_key)):
        return path.glob(file_key)

@error_handling
def list_files() -> None:
    logger.debug("Printing all files")
    for p in BOOK_DIR.rglob("*.txt"):
        print(f"{p}\n")
    if not p:
        logger.debug("Cannot print files, empty directory.")
        print("Empty directory. No files to list.")

def main() -> None:
    delete_book_file("dog")

if __name__ == "__main__":
    main()