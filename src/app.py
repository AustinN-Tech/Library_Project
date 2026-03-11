from flask import Flask, render_template
import database as db

app = Flask(__name__)

data = db.display_all_books()

@app.route("/home")
def home():
    return render_template("index.html", content=data)

if __name__ == "__main__":
    app.run(debug=True)