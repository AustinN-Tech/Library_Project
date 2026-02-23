import database as db
from storage import list_files, write_file, read_file
from utility_functions import (
    get_title, get_author, get_genre, get_OG_filename, get_column, get_value,
    return_formatted_output
)

def terminal_add_book():
    print("-== Add a new Book ==-")
    title = get_title()
    author = get_author()
    genre = get_genre()
    filename = get_OG_filename()
    db.add_book(title, author, genre, filename)

def terminal_delete_book():
    print("-== Delete a Book ==-")
    title = get_title()
    if db.get_book(title) is None:
        print(f"No book found with name {title.title()}")
        return
    db.full_delete(title)

def terminal_update_book():
    title = get_title()
    if db.get_book(title) is None:
        print(f"No book with title: {title.title()} exists.")
        return
    column = get_column()
    value = get_value()
    db.update_book(title, column, value)

def terminal_search_book():
    print("-== Search for a Book ==-\n")
    title = get_title()
    retrieved_book = db.get_book(title)
    if retrieved_book is None:
        print(f"No book found with title {title.title()}")
        return
    print(print(return_formatted_output(retrieved_book[1], retrieved_book[2], retrieved_book[3], retrieved_book[4])))

def terminal_print_all_books():
    print("-== All Books ==-\n")
    data = db.display_all_books()
    if data:
        for i in data:
            print(i, "\n")
    else:
        return

def terminal_delete_all_books():
    print("-== Deleting All Books ==-\n")
    db.delete_all_db()

def terminal_list_book_files():
    print("-== Listing All Files ==-\n")
    list_files()

def terminal_book_write():
    print("-== Write into Book ==-\n")
    title = get_title()
    if db.get_book(title) is None:
        print(f"No book with title: {title.title()} exists.")
        return
    file_key = db.return_file_key(title)
    #content = get_content() # <-- need to make
    #write_file(file_key, content)
    print(f"Content written into {title.title()}.")

def terminal_book_read():
    print("-== Write into Book ==-\n")
    title = get_title()
    if db.get_book(title) is None:
        print(f"No book with title: {title.title()} exists.")
        return
    file_key = db.return_file_key(title)
    content = read_file(file_key)
    print(content)

def terminal_menu():
    while True:
        print("\n-====+ Library Database Menu +====-\n")
        print("Add Book [1]\nDelete Book [2]\nUpdate Book [3]\nSearch for Book [4]\nDisplay all Books [5]\nExit [0]")
        result = input("Enter corresponding number: ").strip()
        print("\n")
        if result == "1":
            terminal_add_book()
        elif result == "2":
            terminal_delete_book()
        elif result == "3":
            terminal_update_book()
        elif result == "4":
            terminal_search_book()
        elif result == "5":
            terminal_print_all_books()
        elif result == "0":
            print("Exiting...\n")
            return False
        else:
            print("Please enter a valid number.")

def terminal_admin_menu():
    pass

def main() -> None:
    terminal_menu()

if __name__ == "__main__":
    main()