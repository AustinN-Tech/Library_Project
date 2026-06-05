from src.app import app
import src.database as db

if __name__ == "__main__":
    db.create_db()
    app.run(debug=True)