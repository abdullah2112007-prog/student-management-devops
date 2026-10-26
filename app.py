from flask import Flask, request

app = Flask(__name__)
students = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            students.append(name)

    student_list = "".join(f"<li>{name}</li>" for name in students)

    return f"""
    <h1>Student Management</h1>
    <form method="post">
        <input name="name" placeholder="Student name" required>
        <button type="submit">Add student</button>
    </form>
    <h2>Students</h2>
    <ul>{student_list}</ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)