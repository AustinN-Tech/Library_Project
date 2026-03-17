from flask import Flask, render_template
from datetime import datetime # for formatting time
import database as db

app = Flask(__name__)

books = db.return_all_books()

for book in books: # formatting time for display
    book.date_added = datetime.fromtimestamp(book.date_added).strftime('%Y-%m-%d')

@app.route("/")
def home():
    return render_template("index.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)