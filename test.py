from app import *

# This function will hold the code for testing the database in the terminal. Needs refactoring.

# redo this function
def prompt_update() -> str:
    print("-== Updating Book ==-\n")
    title = get_title()
    print("\n")

    column = input("Change Data:\nTitle [1]\nAuthor[2]\nGenre[3]\nEnter Number: ")
    while column not in ["1" ,"2", "3"]:
        print("Invalid Choice. Choose from (1-3)")
        column = input("\nChange Data:\nTitle [1]\nAuthor[2]\nEnter Number: ")
    print("\n")
    if column == "1": 
        column = "title"
    elif column == "2":
        column = "author"
    else: 
        column = "genre"

    value = input("Enter new value: ").strip().lower()
    while not value: 
        print("Value cannot be empty. Enter a value.")
        value = input("\nEnter new value: ").strip().lower()
    print("\n")

    return title, column, value

def terminal_menu():
    print("\n-====+ Library Database Menu +====-\n")
    print("Add Book [1]\nDelete Book [2]\nUpdate Book [3]\nSearch for Book [4]\nDisplay all Books [5]\nExit [0]")
    result = int(input("Enter corresponding number: "))
    print("\n")
    if result == 1:
        print("-== Add a new Book ==-")
        title = get_title()
        author = get_author()
        genre = get_genre()
        add_book(title, author, genre)
        terminal_menu()
    elif result == 2:
        print("-== Delete a Book ==-")
        title = get_title()
        if not get_book(title):
            print(f"No book found with name {title}")
            terminal_menu()
        delete_book(title)
        terminal_menu()
    elif result == 3:
        title, column, value = prompt_update()
        update_book(title, column, value)
        terminal_menu()
    elif result == 4:
        print("-== Search for a Book ==-\n")
        title = get_title()
        retrieved_book = get_book(title)
        if not retrieved_book:
            print(f"No book found with title {title}")
            terminal_menu()
        print(return_formatted_output(retrieved_book))
        terminal_menu()
    elif result == 5:
        print("-== All Books ==-\n")
        data = display_all_books()
        for i in data:
            print(i, "\n")
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