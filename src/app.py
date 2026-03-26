from flask import Flask, render_template, send_file, request, redirect, url_for
from datetime import datetime # for formatting time
from storage import return_pdf_file_path, BOOK_DIR
import database as db
import os

app = Flask(__name__)

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
    if not search_results:
        return "No results found"
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
    book_id = request.form["book_id"]
    book = db.get_book_by_id(book_id)
    db.full_delete(book)
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
    if not file_check(file): # safety check on file
        return "Invalid File"
    
    path = os.path.join(BOOK_DIR, file.filename) # obtains path
    file.save(path) # saves file to server

    try: # trys to add file to db, if it fails, then it deletes the file.
        db.add_book(title, author, genre, file.filename, path)
    except Exception:
        os.remove(path)
        return "Error Saving Book"

    return render_template("add_book.html")

# File Checking Functions:
def allowed_filename(filename):
    if not filename.lower().endswith(".pdf"):
        return False
    return True

def check_magic_bytes(file):
    magic_bytes = file.read(5) # obtain first 4 bytes of file (magic bytes which identify file type)
    file.seek(0) # reset file reader

    if not magic_bytes == b"%PDF-": #checks magic_bytes against bytes of %PDF-
        return False
    return True

def file_check(file):
    if file.name == "": return False
    if not allowed_filename(file.filename) or not check_magic_bytes(file):
        return False
    return True

if __name__ == "__main__":
    app.run(debug=True)