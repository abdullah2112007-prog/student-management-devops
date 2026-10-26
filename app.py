import os
import sqlite3
from html import escape
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

DATABASE = os.environ.get("DATABASE_PATH", "students.db")


def initialize_database():
    database_folder = os.path.dirname(DATABASE)
    if database_folder:
        os.makedirs(database_folder, exist_ok=True)

    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            with sqlite3.connect(DATABASE) as connection:
                connection.execute(
                    "INSERT INTO students (name) VALUES (?)",
                    (name,)
                )

        return redirect(url_for("home"))

    with sqlite3.connect(DATABASE) as connection:
        students = connection.execute(
            "SELECT id, name FROM students ORDER BY id"
        ).fetchall()

    student_list = "".join(
        f'<li>{escape(name)} '
        f'<form method="post" action="/delete/{student_id}" style="display:inline;">'
        f'<button type="submit">Delete</button></form></li>'
        for student_id, name in students
    )

    return f"""
    <h1>Student Management</h1>
    <form method="post">
        <input name="name" placeholder="Student name" required>
        <button type="submit">Add student</button>
    </form>
    <h2>Students</h2>
    <ul>{student_list}</ul>
    """


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    return redirect(url_for("home"))


initialize_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)