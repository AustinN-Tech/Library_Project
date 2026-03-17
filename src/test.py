import database as db
from database import Book
from storage import list_files, open_pdf
from utility_functions import (
    get_title, get_author, get_genre, get_OG_filename, get_update_column, get_update_value,
    return_formatted_output, get_path, get_column, get_value, get_order
)

def terminal_get_book() -> Book | None:
    title = get_title()
    book = db.get_book_by_title(title)
    if book is None:
        print(f"No book found with title {title.title()}")
        return None
    return book

def terminal_partial_search() -> list[Book] | None:
    title = get_title()
    search_results = db.partial_search(title)
    if not search_results:
        print(f"No book found with characters: {title}")
        return None
    else:
        return search_results

def terminal_display_results(search_results: list[Book]) -> str | None:
    book_list = {} # for mapping books to indexes
    for i, book in enumerate(search_results, start=1):
        print(f" {book.title.title()} [{i}]")
        book_list[i] = book
    result = input("Enter Corresponding Number (0 to cancel): ").strip()
    if result == "0": # exit condition
        return None

    if not result.isdigit(): # Checking if number was inputted
        print("Invalid input.")
        return None

    book = book_list.get(int(result)) # using .get() so it doesn't crash if not found
    if not book:
        print("Invalid Selection")
        return None
    return book

def terminal_add_book() -> None:
    print("-== Add a new Book ==-")
    # User Inputs:
    title = get_title()
    author = get_author()
    genre = get_genre()
    filename = get_OG_filename()
    path = get_path()

    db.add_book(title, author, genre, filename, path)

def terminal_delete_book() -> None:
    print("-== Delete a Book ==-")
    book = terminal_get_book()
    if not book:
        return
    db.full_delete(book)

def terminal_update_book(book: Book) -> None:
    column = get_update_column()
    if column == "exit":
        return
    value = get_update_value()
    db.update_book(book, column, value)

def print_book_info(book: Book) -> None:
    print(return_formatted_output(book.title, book.author, book.genre, book.date_added))

def terminal_print_all_books() -> None:
    print("-== All Books ==-\n")
    data = db.display_all_books()
    if data:
        for i in data:
            print(i, "\n")
    else:
        return

def terminal_delete_all_books() -> None:
    print("-== Deleting All Books ==-\n")
    answer = input("Are you sure you want to delete all books? [Y/N]: ").strip().lower()
    if answer == "y":
        db.full_delete_all_db()
    elif answer == "n":
        print("Books will not be deleted...\n")
        return
    else:
        print("Invalid Input")

def terminal_list_book_files() -> None:
    print("-== Listing All File Paths ==-\n")
    list_files()

def terminal_PDF_open(book: Book) -> None:
    print("-== Opening File ==-\n")
    open_pdf(book.file_key)

def terminal_book_select_actions(book: Book) -> None:
    while True:
        book = db.get_book_by_id(book.id) # refreshing book object for up to date data entries
        if book is None: # safety check
            print("Book does not exit anymore.\n")
            return
        print("\n")
        print_book_info(book)
        print(" Open [1]\n Update [2]\nBack to Menu [0]")
        result = input("Enter corresponding number: ").strip()
        if result == "1":
            terminal_PDF_open(book)
        elif result =="2":
            terminal_update_book(book)
        elif result == "0":
            print("Back to Menu...\n")
            break
        else:
            print("Please enter a valid number.")

# function to connect terminal display + book functions for selecting books
def terminal_select_book_menu() -> None:
    print("-== Select a Book ==-\n")
    search_results = terminal_partial_search()
    if not search_results:
        return
    print("\n-== Matching Titles ==-")
    book = terminal_display_results(search_results) # obtains title, verifies that it exists in db
    if book is None:
         return
    terminal_book_select_actions(book)

# function to connect terminal display + book functions for filtering books
def terminal_filter_menu() -> None:
    print("-=== Filter ==-")
    search_results = terminal_filter()
    if not search_results:
        return
    book = terminal_display_results(search_results)
    if book is None:
         return
    terminal_book_select_actions(book)

# Obtains users input, returns resulting search results
def terminal_filter() -> list[Book] | None:
    # Obtains users inputs
    column = get_column()
    if column == "genre":
        value = get_genre()
    else: value = get_value()
    order = get_order()
    # Gets and returns search
    search_results = db.filter(column, value, order)
    if not search_results:
        print(f"No books found with specified filter")
        return
    return search_results

"""Main Terminal Menu 
Allows database access (add, delete, update, display, etc...) via terminal.
Primarily for debugging and testing.
"""
def terminal_menu():
    actions = {"1": terminal_add_book, "2": terminal_delete_book, "3": terminal_select_book_menu,
                "4": terminal_print_all_books, "5": terminal_filter_menu, "6": additional_menu}
    while True:
        print("\n-====+ Library Database Menu +====-\n")
        print("  Add Book [1]\n  Delete Book [2]\n  Select Book [3]\n  Display all Books [4]\n  Filter Books [5]\n  Additional Functions [6]\n  Exit [0]")
        result = input("Enter corresponding number: ").strip()
        print("\n")
        if result == "0":
            print("Exiting...")
            break
        func = actions.get(result)
        if func is None:
            print("Please enter a valid number.")
            continue
        func()

# Additional miscellaneous functions such as deleting all books and listing file paths
def additional_menu():
    actions = {"1": terminal_delete_all_books, "2": terminal_list_book_files}
    while True:
        print("\n-== More Functions ==-\n")
        print("  Delete All Books [1]\n  List all Files [2]\n  Back to Menu [0]")
        result = input("Enter corresponding number: ").strip()
        print("\n")
        if result == "0":
            print("Exiting to Menu...")
            break
        func = actions.get(result)
        if func is None:
            print("Please enter a valid number.")
            continue
        func()

def main() -> None:
    terminal_menu()

if __name__ == "__main__":
    main()