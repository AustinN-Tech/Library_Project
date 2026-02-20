from database import *

# This function will hold the code for testing the database in the terminal. Needs refactoring.

def terminal_add_book():
    print("-== Add a new Book ==-")
    title = get_title()
    author = get_author()
    genre = get_genre()
    add_book(title, author, genre)

def terminal_delete_book():
    print("-== Delete a Book ==-")
    title = get_title()
    if not get_book(title):
        print(f"No book found with name {title}")
        terminal_menu()
    delete_book(title)

def terminal_update_book():
    title = get_title()
    column = get_column()
    value = get_value()
    update_book(title, column, value)

def terminal_search_book():
    print("-== Search for a Book ==-\n")
    title = get_title()
    retrieved_book = get_book(title)
    if not retrieved_book:
        print(f"No book found with title {title}")
        terminal_menu()
    print(return_formatted_output(retrieved_book))

def terminal_print_all_books():
    print("-== All Books ==-\n")
    data = display_all_books()
    for i in data:
        print(i, "\n")

def terminal_menu():
    print("\n-====+ Library Database Menu +====-\n")
    print("Add Book [1]\nDelete Book [2]\nUpdate Book [3]\nSearch for Book [4]\nDisplay all Books [5]\nExit [0]")
    result = int(input("Enter corresponding number: "))
    print("\n")
    if result == 1:
        terminal_add_book()
        terminal_menu()
    elif result == 2:
        terminal_delete_book()
        terminal_menu()
    elif result == 3:
        terminal_update_book()
        terminal_menu()
    elif result == 4:
        terminal_search_book()
        terminal_menu()
    elif result == 5:
        terminal_print_all_books()
        terminal_menu()
    elif result == 0:
        print("Exiting...\n")
        return
    else:
        print("Please enter a valid number.")


def main() -> None:
    add_book("Test 1".lower(), "John Doe".lower(), "horror")

    add_book("Test 2".lower(), "Jane Doe".lower(), "adventure")

    terminal_menu()


if __name__ == "__main__":
    main()