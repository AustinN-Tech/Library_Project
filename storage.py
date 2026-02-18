from pathlib import Path
from utility_functions import create_file_key

BASE_DIR = Path(__file__).resolve().parent # takes the absolute path of the parent folder of code file
BOOK_DIR = BASE_DIR / "book_pdfs"

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
    else:
        raise FileNotFoundError(f"File: {file_key} cannot be found.")

def rename_file_key(old_file_key: str, new_file_key: str) -> Path:
    old_path = return_file_path(old_file_key)
    new_path = return_file_path(new_file_key)
    if not old_path.exists(): # if old path not found, raise error
       raise FileNotFoundError(f"Path: {old_path} cannot be found.") 
    return old_path.rename(new_path)

def get_directory(Directory) -> Path:
    return Path(Directory).resolve()

def write_file(file_key: str, input: str) -> None:
    path = return_file_path(file_key)
    with open(path, 'w') as f:
        f.write(input)

def read_file(file_key: str) -> None:
    path = return_file_path(file_key)
    with open(path, 'r') as f:
        print(f.read())

def file_return(file_key: str, directory: str) -> Path | None:
    path = return_file_path(file_key)
    if (path.glob(file_key)):
        return path.glob(file_key)

def list_files() -> None:
    for p in BOOK_DIR.rglob("*.txt"):
        print(f"{p}\n")
    if not p:
        print("Empty directory. No files to list.")

def main() -> None:
    # testing file key: "book_1771354641_6a2c.txt"
    # read_file("book_1771354641_6a2c.txt")
    delete_book_file("book_1771355090_f62a.txt")

if __name__ == "__main__":
    main()

