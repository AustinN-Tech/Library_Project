from pathlib import Path
from utility_functions import create_file_key

# The File Management will be Setup Here

BOOK_DIR = Path.home() / "book_pdfs" # shouldn't be Path.home() long term

def create_book_directory() -> None:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)

def return_file_path(file_key: str) -> Path:
    if Path(file_key).name != file_key:
        raise ValueError("file_key must be a filename only")
    path = BOOK_DIR / file_key
    return path

def create_book_file() -> str:
    create_book_directory() # makes a directory is there isn't one
    file_key = create_file_key() # makes unique file_key
    path = return_file_path(file_key)
    path.touch(exist_ok=False) # creates file
    return file_key

def delete_book_file(file_key: str) -> None:
    path = return_file_path(file_key)
    if path.exists():
        path.unlink()

def rename_file_key(old_file_key: str, new_file_key: str) -> Path:
    old_path = return_file_path(old_file_key)
    new_path = return_file_path(new_file_key)
    if not old_path.exists(): # if old path not found, raise error
       raise FileNotFoundError(old_path) 
    return old_path.rename(new_path)

def write_file():
    pass

def open_file():
    pass

def file_search(file_key: str, directory: str):
    pass



def main() -> None:
    pass

if __name__ == "__main__":
    main()

