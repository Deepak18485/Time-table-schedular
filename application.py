from flask import Flask, render_template, request, redirect
from datetime import datetime
from collections import defaultdict
from Schedular import EnhancedScheduler
import mysql.connector
import os

app = Flask(__name__)

# ✅ MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Use your actual MySQL password here
    database="timetable"
)
cursor = conn.cursor()

# ✅ Redirect base URL to form
@app.route("/")
def home():
    return redirect("/input")

# ✅ Input form route
@app.route("/input")
def input_page():
    cursor.execute("SELECT Subname FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM teachers")
    teachers = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT room_name FROM rooms")
    rooms = [row[0] for row in cursor.fetchall()]

    return render_template("input.html", subjects=subjects, teachers=teachers, rooms=rooms)

# ✅ Schedule generation route
@app.route("/generate", methods=["POST"])
def generate_schedule_display():
    try:
        # Time and lecture slot logic
        start_time_str = request.form.get("start_time")
        end_time_str = request.form.get("end_time")
        lecture_duration = int(request.form.get("lecture_duration"))
        working_days = request.form.getlist("working_days")

        fmt = "%H:%M"
        start_dt = datetime.strptime(start_time_str, fmt)
        end_dt = datetime.strptime(end_time_str, fmt)
        total_hours = int((end_dt - start_dt).total_seconds() // 3600)

        # Groups and Rooms
        groups = request.form.getlist("groups[]")
        rooms = request.form.getlist("rooms[]")

        # Subjects
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

        # 🧠 Create scheduler
        scheduler = EnhancedScheduler(
            subjects=subjects,
            student_groups=groups,
            rooms=rooms,
            working_days=working_days,
            hours_per_day=total_hours,
            lecture_duration=lecture_duration
        )

        # Override time_slots with actual usable slots
        slots_per_day = total_hours // lecture_duration
        scheduler.time_slots = [(day, slot) for day in working_days for slot in range(slots_per_day)]

        # Algorithm selector (greedy or backtracking)
        algorithm = request.form.get("algorithm", "auto")
        if algorithm == "greedy":
            success = scheduler.generate_schedule_greedy()
        else:
            success = scheduler.generate_schedule()

        # Return output
        if success and scheduler.schedule:
            schedule = structure_schedule_for_display(scheduler)
            scheduler.export_to_csv("static/generated_schedule.csv")

            return render_template(
                "success.html",
                schedule=schedule,
                slots_per_day=slots_per_day,
                working_days=working_days,
                file_path="static/generated_schedule.csv"
            )
        else:
            return render_template("error.html", message="❌ Failed to generate schedule.")
    
    except Exception as e:
        return render_template("error.html", message=f"Error: {str(e)}")

# ✅ Utility: Format for table rendering
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

# ✅ Start server
if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
