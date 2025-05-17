from flask import Flask, render_template, request, redirect, url_for
from Schedular import EnhancedScheduler  # Your custom scheduling class

app = Flask(__name__)

# Dummy login credentials
USERNAME = "admin"
PASSWORD = "admin123"

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
    return render_template("input.html")

@app.route("/generate", methods=["POST"])
def generate_schedule():
    # Collecting form data
    working_days = request.form.getlist("working_days")
    hours_per_day = int(request.form.get("hours_per_day"))
    lecture_duration = int(request.form.get("lecture_duration"))
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
        hours_per_day=hours_per_day,
        lecture_duration=lecture_duration
    )

    success = scheduler.generate_schedule_greedy()

    if success:
        scheduler.export_to_csv("C:/Users/MANISH/OneDrive/Desktop/Project/PBL(DAA)/DAA-PBL/DAA-Project/static/generated_schedule.csv")
        return render_template("success.html")
    else:
        return "Could not generate schedule", 500

if __name__ == "__main__":
    app.run(debug=True)
