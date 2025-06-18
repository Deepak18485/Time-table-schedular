from flask import Flask, render_template, request, redirect, url_for
from Schedular import EnhancedScheduler  # Your custom scheduling class
from schedule_display import generate_schedule_display, structure_schedule_for_display

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
        scheduler.export_to_csv("static/generated_schedule.csv")
        structured_schedule = structure_schedule_for_display(scheduler)  
        return render_template(
            "success.html",
            schedule=structured_schedule,
            slots_per_day=scheduler.slots_per_day,
            working_days=scheduler.working_days,
            file_path="static/generated_schedule.csv"
        )
    else:
        return render_template("error.html", message="Failed to generate schedule.")



if __name__ == "__main__":
    app.run(debug=True)
