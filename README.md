# SQLing Hellos

A Flask and SQLAlchemy Coursework Example for Advances in Software Engineering

A small Flask web app where you can say hello to a name in a simple, styled box.

## How to run locally

These steps get the app running on your machine.

### 1. Clone the repository

```bash
git clone git@github.com:EDGENortheastern/aise-c-example1.git
cd aise-c-example1
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows, activate with `venv\Scripts\activate` instead.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database tables

This app uses a local SQLite database. Create the tables once before running
the app for the first time:

```bash
flask --app app init-db
```

This creates `instance/app.db` with the `user` table. The `instance/` folder
(and the database file inside it) is excluded from version control by
`.gitignore`, so the database is never committed to GitHub.

### 5. Run the app

```bash
python app.py
```

### 6. View it in the browser

Open:

```text
http://127.0.0.1:5000
```

To stop the server, press `Ctrl+C`.
