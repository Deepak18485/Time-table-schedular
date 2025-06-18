from flask import Flask, render_template, request, redirect, url_for
from Schedular import EnhancedScheduler
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='timetable'
)
cursor = conn.cursor()

USERNAME = "admin"
PASSWORD = "admin123"

def clear_cursor():
    try:
        cursor.fetchall()
    except:
        pass

@app.route("/")
def index():
    return redirect(url_for("admin_login"))

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("input_page"))
        else:
            return "Invalid login", 401
    return render_template("admin.html")

@app.route("/input")
def input_page():
    clear_cursor()
    cursor.execute("SELECT Subname FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]

    clear_cursor()
    cursor.execute("SELECT name FROM teachers")
    teachers = [row[0] for row in cursor.fetchall()]

    clear_cursor()
    cursor.execute("SELECT room_name FROM rooms")
    rooms = [row[0] for row in cursor.fetchall()]

    return render_template("input.html", subjects=subjects, teachers=teachers, rooms=rooms)

@app.route("/generate", methods=["POST"])
def generate_schedule():
    # Time range input
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    working_days = request.form.getlist("working_days")

    # Filter timeslots from DB within selected time range
    clear_cursor()
    cursor.execute("""
        SELECT day, slot_id FROM timeslots
        WHERE start_time >= %s AND end_time <= %s
    """, (start_time, end_time))
    timeslot_results = cursor.fetchall()

    # Convert to format: [('Monday', 0), ('Monday', 1), ...]
    time_slots = [(row[0], row[1]) for row in timeslot_results]

    # Collecting form data
    groups = request.form.getlist("groups[]")
    rooms = request.form.getlist("rooms[]")
    subject_names = request.form.getlist("subject_name[]")
    teachers = request.form.getlist("teacher[]")
    sessions = request.form.getlist("sessions[]")
    types = request.form.getlist("type[]")
    lecture_duration = int(request.form.get("lecture_duration"))

    # Build subjects dictionary
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
        hours_per_day=0,  # not used now
        lecture_duration=lecture_duration
    )
    # Replace internal time_slots
    scheduler.time_slots = time_slots

    success = scheduler.generate_schedule()

    if success and scheduler.schedule:
        # Build table data
        schedule_data = []
        for (subject, group, session_index), (day, slot, room) in sorted(
            scheduler.schedule.items(), key=lambda x: (x[1][0], x[1][1])
        ):
            teacher = scheduler.subjects[subject]['teacher']
            schedule_data.append({
                'day': day,
                'slot': f"Slot {slot + 1}",
                'group': group,
                'subject': subject,
                'teacher': teacher,
                'room': room,
                'session': session_index + 1
            })

        return render_template("success.html", schedule=schedule_data)
    else:
        return render_template("error.html", message="Failed to generate schedule, even with backtracking.")

if __name__ == "__main__":
    app.run(debug=True)
