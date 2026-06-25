import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# The database URL can be overridden with the DATABASE_URL environment
# variable (e.g. in tests or deployment). It defaults to a local SQLite
# file stored in the app's instance/ folder.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Used to sign the session cookie so flash messages work. Override in
# production with the SECRET_KEY environment variable.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


# Create the local database tables. Run this once before starting the app
# for the first time:
#
#     flask --app app init-db
#
# It creates instance/app.db (ignored by git) with the tables for every
# model defined above, including User.
@app.cli.command("init-db")
def init_db_command():
    """Create the database tables."""
    db.create_all()
    print("Initialized the database and created the tables.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        # All fields are required.
        if not username or not email or not password:
            flash("Please fill in every field.", "error")
            return render_template("register.html", username=username, email=email)

        # Give a clear message if the username or email is already taken,
        # rather than letting the database constraint raise an error.
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing is not None:
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email)

        # Never store the raw password - hash it before saving.
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            # Safety net if two people register the same details at once.
            db.session.rollback()
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email)

        flash(f"Welcome, {username}! Your account has been created.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        # Check the submitted details against the stored user.
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            # Same message either way so we don't reveal which usernames exist.
            flash("Invalid username or password.", "error")
            return render_template("login.html", username=username)

        # Keep the user logged in for the rest of the browser session.
        session["user_id"] = user.id
        session["username"] = user.username
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)