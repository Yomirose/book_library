from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

# create the app
app = Flask(__name__)

# configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# initialize the app
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    books = Book.query.all()
    if not books:
        return render_template("index.html", empty_library=True)
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_books = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_books)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    update_book =db.get_or_404(Book, book_id)
    if request.method == "POST":
        new_rating = request.form["new_rating"]
        update_book.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", update_book=update_book)


@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id):
    book_to_delete = db.get_or_404(Book, book_id)
    if request.method == "POST":
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("delete.html", book_to_delete=book_to_delete)

if __name__ == "__main__":
    app.run(debug=True)

