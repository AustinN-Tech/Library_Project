import os
import fitz # for obtaining cover path (first page of PDF)
from pathlib import Path
from src.utility_functions import create_file_key, error_handling, initialize_logging
from shutil import copy2

BASE_DIR = Path(__file__).resolve().parent.parent # takes the absolute path of the parent folder of code file
BOOK_DIR = BASE_DIR / "book_pdfs"
STATIC_DIR = BASE_DIR / "src" / "static"
COVER_DIR = STATIC_DIR / "images" / "book_covers"

logger = initialize_logging() # setting logging

@error_handling
def create_book_directory() -> None:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directory Created {get_directory(BOOK_DIR)}")

@error_handling
def return_pdf_file_path(file_key: str) -> Path:
    if Path(file_key).name != file_key:
        raise ValueError(f"Attempted file_key: {file_key} is incorrect. file_key must be a filename only")
    path = BOOK_DIR / file_key
    logger.debug(f"Returned Path {file_key} -> {path}")
    return path

@error_handling
def delete_book_file(file_key: str) -> None:
    path = return_pdf_file_path(file_key)
    if path.exists():
        path.unlink()
        logger.debug(f"File {file_key} at {path} fully deleted")
    else:
        raise FileNotFoundError(f"File {file_key} cannot be found.")

@error_handling
def rename_file_key(old_file_key: str, new_file_key: str) -> Path:
    old_path = return_pdf_file_path(old_file_key)
    new_path = return_pdf_file_path(new_file_key)
    if not old_path.exists(): # if old path not found, raise error
       raise FileNotFoundError(f" Path {old_path} cannot be found.") 
    logger.debug(f"{old_file_key} renamed to {new_file_key} successfully")
    return old_path.rename(new_path)

def get_directory(Directory) -> Path:
    return Path(Directory).resolve()

@error_handling
def create_book_pdf(original_path: Path) -> str:
    create_book_directory() # makes a directory is there isn't one

    file_key = create_file_key(file_type="pdf")
    new_path = return_pdf_file_path(file_key)
    copy2(original_path, new_path)
    logger.debug(f"File {file_key} created at {new_path}")
    return file_key

@error_handling
def open_pdf(file_key: str) -> None:
    filepath = BOOK_DIR / file_key # accessing directory of book_pdfs
    if not filepath.exists(): # checking if it is found
        print("File Not Found")
        logger.debug(f"Filepath: {filepath} not found")
        return
    os.startfile(filepath)
    logger.debug(f"Opened PDF from {filepath}")

@error_handling
def file_return(file_key: str) -> Path | None:
    path = return_pdf_file_path(file_key)
    if path.exists():
        return path

@error_handling
def list_files() -> None:
    logger.debug("Printing all files")
    for p in BOOK_DIR.rglob("*.pdf"):
        print(f"{p}\n")
    if not p:
        logger.debug("Cannot print files, empty directory.")
        print("Empty directory. No files to list.")

@error_handling
def generate_cover(pdf_path: Path, file_key: str) -> str:
    clean_key = Path(file_key).stem # gets rid of ".pdf", temporary fix
    output_path = COVER_DIR / f"{clean_key}.png" # create output path

    output_path.parent.mkdir(parents=True, exist_ok=True) # check if directory exists

    with fitz.open(pdf_path) as doc:
        page = doc.load_page(0) # index first page of doc for cover
        matrix = fitz.Matrix(2, 2) # increase resolution
        pix = page.get_pixmap(matrix=matrix) # turn into image
        pix.save(output_path)

    logger.debug(f"Created Cover Path for {file_key}")
    return output_path.relative_to(STATIC_DIR).as_posix() # need to be relative path for flask to serve image, "as_posix()" swaps the direction of the slashes (/) making it into a format flask can use

@error_handling
def return_absolute_cover_path(cover_path: Path) -> Path:
    return STATIC_DIR / cover_path

@error_handling
def change_cover_file(old_cover_path: Path, new_cover_path: Path):
    if not new_cover_path.exists(): # if new cover not found, raise error
       raise FileNotFoundError(f" Path {new_cover_path} cannot be found.")
    new_cover_path.replace(return_absolute_cover_path(old_cover_path)) # old path is obtained via db, so it is relative. Needs to be converted to absolute before replacement

@error_handling
def delete_book_cover(cover_path: Path) -> None:
    path = return_absolute_cover_path(cover_path) # gets absolute file path, needed for deletion
    if path.exists():
        path.unlink()
        logger.debug(f"File {cover_path} at {path} fully deleted")
    else:
        raise FileNotFoundError(f"File {cover_path} cannot be found.")

def main() -> None:
    pass

if __name__ == "__main__":
    main()