from flask import Flask, render_template, send_file
from datetime import datetime # for formatting time
from storage import return_pdf_file_path
import database as db

app = Flask(__name__)

books = db.return_all_books()

for book in books: # formatting time for display
    book.date_added = datetime.fromtimestamp(book.date_added).strftime('%Y-%m-%d')

@app.route("/")
def home():
    return render_template("index.html", books=books)

@app.route("/books/<id>")
def open_book(id):
    book = db.get_book_by_id(id)
    path = return_pdf_file_path(book.file_key)
    return send_file(path_or_file=path, download_name=book.original_filename)

if __name__ == "__main__":
    app.run(debug=True)