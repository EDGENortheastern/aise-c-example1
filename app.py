import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The database URL can be overridden with the DATABASE_URL environment
# variable (e.g. in tests or deployment). It defaults to a local SQLite
# file stored in the app's instance/ folder.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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


if __name__ == "__main__":
    app.run(debug=True)