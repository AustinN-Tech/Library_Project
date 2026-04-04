from flask import Flask, render_template, send_file, request, redirect, url_for, flash
from datetime import datetime # for formatting time
from storage import return_pdf_file_path, change_cover_file, BOOK_DIR, COVER_DIR
from utility_functions import initialize_logging, book_file_check, cover_file_check
import database as db
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)

logger = initialize_logging() # setting logging

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/home")
def home():
    books = db.return_all_books()
    for book in books: # formatting time for display
        book.date_added = datetime.fromtimestamp(book.date_added).strftime('%Y-%m-%d')
    return render_template("index.html", books=books)

@app.route("/search", methods=['POST'])
def search():
    search_input = request.form["search_input"]
    column = request.form["column"]
    order = request.form["order"]
    search_results = db.global_search(column, search_input, order)
    for book in search_results: # formatting time for display
        book.date_added = datetime.fromtimestamp(book.date_added).strftime('%Y-%m-%d')
    return render_template("index.html", books=search_results)

@app.route("/books/<id>")
def open_book(id):
    book = db.get_book_by_id(id)
    path = return_pdf_file_path(book.file_key)
    return send_file(path_or_file=path, download_name=book.original_filename)

@app.route("/delete", methods=["POST"])
def delete_action():
    logger.debug("Attempting delete of book (flask)...")
    book_id = request.form["book_id"]
    book = db.get_book_by_id(book_id)
    try:
        db.full_delete(book)
        logger.debug("Deleted book, returning home page...")
        flash("Delete Successful", "success")
    except:
        flash("Error: Deletion Error", "error")
    finally:
        return redirect(url_for("home"))

@app.route("/add_book")
def add_book_page():
    return render_template("add_book.html")

@app.route("/add", methods=['POST'])
def add_action():
    title = request.form["title"]
    author = request.form["author"]
    genre = request.form["genre"]
    file = request.files["book_file"]
    if not book_file_check(file): # safety check on file
        flash("Error: Invalid File", "error")
        return render_template("add_book.html")
    
    path = Path(BOOK_DIR) / file.filename
    file.save(path)

    try: # trys to add file to db, if it fails, then it deletes the file.
        db.add_book(title, author, genre, file.filename, path)
    except Exception:
        flash(f"Error: {title.title()} could not be added", "error")
        return render_template("add_book.html")
    finally:
        os.remove(path) # delete old original file uploaded by user

    flash(f"{title.title()} Added", "success")
    return render_template("add_book.html")

"""
Gets current book id (the book where 'Update Info' was pressed) and passes it so that
the current book is at the top of the dropdown for 'Select Book' in the update_book page
it also deletes it from the larger list so it doesn't end up repeating
--> Will add JS later to revamp the update_book
"""
@app.route("/update_book", methods=['POST'])
def update_book_page():
    book_id = request.form["book_id"]
    book = db.get_book_by_id(book_id)
    all_books = db.return_all_books()
    if book in all_books:
        all_books.remove(book)
    return render_template("update_book.html", books=all_books, current_book=book)

@app.route("/update", methods=['POST'])
def update_action():
    book_id = request.form["book_id"]
    column = request.form["column"]
    value = request.form["update_value"]
    book = db.get_book_by_id(book_id)
    try:
        db.update_book(book, column, value)
    except Exception:
        flash("Error: Update Failed", "error")
        return redirect(url_for("home"))
    
    flash("Update Successful", "success")
    return redirect(url_for("home"))

@app.route("/change_cover", methods=['POST'])
def change_cover():
    book_id = request.form["book_id"]
    book = db.get_book_by_id(book_id)
    cover_file = request.files["cover_file"]
    if not cover_file_check(cover_file): # safety check on file
        flash("Error: Invalid Cover File", "error")
        return redirect(url_for("home"))

    path = Path(COVER_DIR) / cover_file.filename
    cover_file.save(path)

    try:
        change_cover_file(book.cover_path, path)
    except Exception:
        os.remove(path) # delete old original file uploaded by user
        flash("Error: Cover Changed Unsuccessful", "error")
        return redirect(url_for("home"))


    flash("Cover Updated", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)