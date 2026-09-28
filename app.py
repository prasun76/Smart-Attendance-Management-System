import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
DB = os.environ.get("DATABASE_PATH", "attendance.db")


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL UNIQUE,
        branch TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        att_date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Present','Absent')),
        UNIQUE(student_id, att_date),
        FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()


@app.get("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    total = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
    present = conn.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'").fetchone()[0]
    conn.close()
    overall = round(present * 100 / total, 1) if total else 0
    return render_template("index.html", students=students, overall=overall,
                           total=total, present=present, today=date.today().isoformat())


@app.post("/add_student")
def add_student():
    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    branch = request.form.get("branch", "").strip()
    if not all((name, roll_no, branch)):
        flash("All student fields are required.", "error")
        return redirect(url_for("index"))
    conn = get_db()
    try:
        conn.execute("INSERT INTO students(name, roll_no, branch) VALUES(?,?,?)",
                     (name, roll_no, branch))
        conn.commit()
        flash("Student added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Roll number already exists.", "error")
    finally:
        conn.close()
    return redirect(url_for("index"))


@app.post("/mark_attendance")
def mark_attendance():
    att_date = request.form.get("att_date", date.today().isoformat())
    conn = get_db()
    students = conn.execute("SELECT id FROM students").fetchall()
    for student in students:
        status = request.form.get(f"status_{student['id']}")
        if status in ("Present", "Absent"):
            conn.execute("""INSERT INTO attendance(student_id, att_date, status)
                VALUES(?,?,?)
                ON CONFLICT(student_id, att_date)
                DO UPDATE SET status=excluded.status""",
                (student["id"], att_date, status))
    conn.commit()
    conn.close()
    flash("Attendance saved successfully.", "success")
    return redirect(url_for("index"))


@app.get("/report")
def report():
    conn = get_db()
    students = conn.execute("""
        SELECT s.id, s.name, s.roll_no, s.branch,
               COUNT(a.id) AS total,
               COALESCE(SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END), 0) AS present
        FROM students s
        LEFT JOIN attendance a ON s.id=a.student_id
        GROUP BY s.id
        ORDER BY s.roll_no
    """).fetchall()
    conn.close()
    rows = []
    for s in students:
        total = s["total"] or 0
        present = s["present"] or 0
        pct = round(present * 100 / total, 1) if total else 0
        rows.append({**dict(s), "percentage": pct})
    return render_template("report.html", rows=rows)


@app.post("/delete/<int:student_id>")
def delete_student(student_id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted.", "success")
    return redirect(url_for("index"))


@app.get("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(debug=True)
