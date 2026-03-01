import database as db
from storage import list_files, open_pdf
from utility_functions import (
    get_title, get_author, get_genre, get_OG_filename, get_column, get_value,
    return_formatted_output, get_path
)

def terminal_get_title() -> str | None:
    title = get_title()
    if db.get_book(title) is None: # verifies title exists in db
        print(f"No book found with title {title.title()}")
        return
    return title

def terminal_partial_search() -> list[tuple] | None:
    title = get_title()
    search_results = db.partial_search(title)
    if not search_results:
        print(f"No book found with characters: {title}")
        return
    else:
        return search_results

def terminal_display_partial_search(search_results: list[tuple]) -> str | None:
    print("\n-== Matching Titles ==-")
    book_list = {} # for mapping titles to indexes
    for i, row in enumerate(search_results, start=1):
        print(f" {row[1].title()} [{i}]")
        book_list[i] = row[1]
    result = input("Enter Corresponding Number (0 to cancel): ").strip()
    if result == "0": # exit condition
        return

    if not result.isdigit(): # Checking if number was inputted
        print("Invalid input.")
        return

    title = book_list.get(int(result)) # using .get() so it doesn't crash if not found
    if not title:
        print("Invalid Selection")
        return
    return title

def terminal_add_book():
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
    title = terminal_get_title()
    if not title:
        return
    db.full_delete(title)

def terminal_update_book(title: str) -> None:
    column = get_column()
    value = get_value()
    db.update_book(title, column, value)

def print_book_info(title: str) -> None:
    retrieved_book = db.get_book(title)
    print(return_formatted_output(retrieved_book[1], retrieved_book[2], retrieved_book[3], retrieved_book[4]))

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

def terminal_list_book_files():
    print("-== Listing All File Paths ==-\n")
    list_files()

def terminal_PDF_open(title: str) -> str:
    print("-== Opening File ==-\n")
    file_key = db.return_file_key(title)
    open_pdf(file_key)

def terminal_select_book_menu():
    print("-== Select a Book ==-\n")
    title = terminal_display_partial_search(terminal_partial_search()) # obtains title, verifies that it exists in db
    if title is None:
         return
    while True:
        print("\n")
        print_book_info(title)
        print(" Open [1]\n Update [2]\nBack to Menu [0]")
        result = input("Enter corresponding number: ").strip()
        if result == "1":
            terminal_PDF_open(title)
        elif result =="2":
            terminal_update_book(title)
        elif result == "0":
            print("Back to Menu...\n")
            break
        else:
            print("Please enter a valid number.")

"""Main Terminal Menu 
Allows database access (add, delete, update, display, etc...) via terminal.
Primarily for debugging and testing.
"""
def terminal_menu():
    while True:
        print("\n-====+ Library Database Menu +====-\n")
        print("  Add Book [1]\n  Delete Book [2]\n  Select Book [3]\n  Display all Books [4]\n  Additional Functions [5]\n  Exit [0]")
        result = input("Enter corresponding number: ").strip()
        print("\n")
        if result == "1":
            terminal_add_book()
        elif result == "2":
            terminal_delete_book()
        elif result == "3":
            terminal_select_book_menu()
        elif result == "4":
            terminal_print_all_books()
        elif result == "5":
            additional_menu()
        elif result == "0":
            print("Exiting...\n")
            break
        else:
            print("Please enter a valid number.")

# Additional miscellaneous functions such as deleting all books and listing file paths
def additional_menu():
    while True:
        print("\n-== More Functions ==-\n")
        print("  Delete All Books [1]\n  List all Files [2]\n  Back to Menu [0]")
        result = input("Enter corresponding number: ").strip()
        print("\n")
        if result == "1":
            terminal_delete_all_books()
        elif result == "2":
            terminal_list_book_files()
        elif result == "0":
            print("Back to Menu...\n")
            break
        else:
            print("Invalid number.")
            return

def main() -> None:
    terminal_menu()

if __name__ == "__main__":
    main()