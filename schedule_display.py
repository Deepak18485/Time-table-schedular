from flask import request, render_template
from collections import defaultdict
from Schedular import EnhancedScheduler


def structure_schedule_for_display(scheduler):
    # Creates a nested dictionary: schedule[group][day][slot] = session info
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


def generate_schedule_display():
    # Read form data
    working_days = request.form.getlist("working_days")
    hours_per_day = int(request.form.get("hours_per_day"))
    lecture_duration = int(request.form.get("lecture_duration"))
    groups = request.form.getlist("groups[]")
    rooms = request.form.getlist("rooms[]")

    subject_names = request.form.getlist("subject_name[]")
    teachers = request.form.getlist("teacher[]")
    sessions = request.form.getlist("sessions[]")
    types = request.form.getlist("type[]")

    # Construct subject dictionary
    subjects = {}
    for i in range(len(subject_names)):
        subjects[subject_names[i]] = {
            "teacher": teachers[i],
            "sessions_per_week": int(sessions[i]),
            "type": types[i]
        }

    # Create scheduler
    scheduler = EnhancedScheduler(
        subjects=subjects,
        student_groups=groups,
        rooms=rooms,
        working_days=working_days,
        hours_per_day=hours_per_day,
        lecture_duration=lecture_duration
    )

    # Choose algorithm
    algorithm = request.form.get("algorithm")
    if algorithm == "greedy":
        success = scheduler.generate_schedule_greedy()
    else:
        try:
            success = scheduler.generate_schedule()  # Only if implemented
        except AttributeError:
            success = False

    # Generate response
    if success and scheduler.schedule:
        structured_schedule = structure_schedule_for_display(scheduler)
        csv_path = "static/generated_schedule.csv"
        scheduler.export_to_csv(csv_path)

        return render_template(
            'success.html',
            schedule=structured_schedule,
            slots_per_day=scheduler.slots_per_day,
            working_days=scheduler.working_days,
            file_path=csv_path
        )
    else:
        return render_template("error.html", message="Failed to generate schedule.")
