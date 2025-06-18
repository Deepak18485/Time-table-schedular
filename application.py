from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from collections import defaultdict
from Schedular import EnhancedScheduler
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Set your MySQL root password if needed
    database="timetable"
)
cursor = conn.cursor()

# Redirect root to admin login
@app.route("/")
def home_redirect():
    return redirect("/admin")

# Admin login route
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            flash("Invalid credentials", "error")
    return render_template("admin_login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/admin")

# Admin dashboard route
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/admin")
    return render_template("admin_dashboard.html")

# Add subject route
@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if not session.get("logged_in"):
        return redirect("/admin")
    if request.method == "POST":
        name = request.form.get("subject_name")
        cursor.execute("INSERT INTO subjects (Subname) VALUES (%s)", (name,))
        conn.commit()
        return redirect("/dashboard")
    return render_template("add_subject.html")

# Add teacher route
@app.route("/add_teacher", methods=["GET", "POST"])
def add_teacher():
    if not session.get("logged_in"):
        return redirect("/admin")
    if request.method == "POST":
        name = request.form.get("teacher_name")
        cursor.execute("INSERT INTO teachers (name) VALUES (%s)", (name,))
        conn.commit()
        return redirect("/dashboard")
    return render_template("add_teacher.html")

# Add room route
@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if not session.get("logged_in"):
        return redirect("/admin")
    if request.method == "POST":
        name = request.form.get("room_name")
        cursor.execute("INSERT INTO rooms (room_name) VALUES (%s)", (name,))
        conn.commit()
        return redirect("/dashboard")
    return render_template("add_room.html")

# View tables route
@app.route("/view_tables")
def view_tables():
    if not session.get("logged_in"):
        return redirect("/admin")
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    return render_template("view_tables.html", subjects=subjects, teachers=teachers, rooms=rooms)

# Input form route
@app.route("/input")
def input_page():
    if not session.get("logged_in"):
        return redirect("/admin")
    cursor.execute("SELECT Subname FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT name FROM teachers")
    teachers = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT room_name FROM rooms")
    rooms = [row[0] for row in cursor.fetchall()]
    return render_template("input.html", subjects=subjects, teachers=teachers, rooms=rooms)

# Generate schedule route
@app.route("/generate", methods=["POST"])
def generate_schedule_display():
    try:
        start_time_str = request.form.get("start_time")
        end_time_str = request.form.get("end_time")
        lecture_duration = int(request.form.get("lecture_duration"))
        working_days = request.form.getlist("working_days")
        fmt = "%H:%M"
        start_dt = datetime.strptime(start_time_str, fmt)
        end_dt = datetime.strptime(end_time_str, fmt)
        total_hours = int((end_dt - start_dt).total_seconds() // 3600)

        groups = request.form.getlist("groups[]")
        rooms = request.form.getlist("rooms[]")
        subject_names = request.form.getlist("subject_name[]")
        teachers = request.form.getlist("teacher[]")
        sessions = request.form.getlist("sessions[]")
        types = request.form.getlist("type[]")

        subjects = {}
        for i in range(len(subject_names)):
            subjects[subject_names[i]] = {
                "teacher": teachers[i],
                "sessions_per_week": int(sessions[i]),
                "type": types[i]
            }

        scheduler = EnhancedScheduler(
            subjects=subjects,
            student_groups=groups,
            rooms=rooms,
            working_days=working_days,
            hours_per_day=total_hours,
            lecture_duration=lecture_duration
        )

        slots_per_day = total_hours // lecture_duration
        scheduler.time_slots = [(day, slot) for day in working_days for slot in range(slots_per_day)]

        algorithm = request.form.get("algorithm", "auto")
        success = scheduler.generate_schedule_greedy() if algorithm == "greedy" else scheduler.generate_schedule()

        if success and scheduler.schedule:
            schedule = structure_schedule_for_display(scheduler)
            scheduler.export_to_csv("static/generated_schedule.csv")
            return render_template("success.html", schedule=schedule, slots_per_day=slots_per_day,
                                   working_days=working_days, file_path="static/generated_schedule.csv")
        else:
            return render_template("error.html", message="❌ Failed to generate schedule.")

    except Exception as e:
        return render_template("error.html", message=f"Error: {str(e)}")

# Structure for table rendering
def structure_schedule_for_display(scheduler):
    structured = defaultdict(lambda: defaultdict(dict))
    for (subject, group, session_index), (day, slot, room) in scheduler.schedule.items():
        teacher = scheduler.subjects[subject]['teacher']
        structured[group][day][slot] = {
            'subject': subject,
            'teacher': teacher,
            'room': room,
            'session': session_index + 1
        }
    return structured

# Start the Flask app
if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)