from pathlib import Path

# The File Management will be Setup Here

def create_book_directory() -> None:
    p = Path.home() / "book_pdfs"
    p.mkdir(exist_ok=True)

