from datetime import datetime

def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Error: ", e)
    return wrapper

def get_title():
    title = input("Enter title of book: ").strip().lower()
    while not title:
        print("Title cannot be empty. Enter a title.")
        title = input("\nEnter title of book: ").strip().lower()

    return title

def get_author():
    author = input("Enter author of book: ").strip().lower()
    if not author: 
        author = "unknown"

    return author

def get_genre():
    genre = input("Enter genre of book: ").strip().lower()
    while not genre:
        print("Genre cannot be empty. Enter a genre.")
        genre = input("\nEnter genre of book: ").strip().lower()

    return genre

def return_formatted_output(title, author, genre, date_added):
    dt = datetime.fromtimestamp(date_added) # formatting time to datetime
    formatted_output = f"Book Title: {title.title()}\nBook Author: {author.title()}\nGenre: {genre.title()}\nDate Added: {dt.strftime('%Y-%m-%d')}"
    return formatted_output