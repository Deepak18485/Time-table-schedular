import os
import csv

class EnhancedScheduler:
    def __init__(self, subjects, student_groups, rooms, working_days, hours_per_day, lecture_duration):
        self.subjects = subjects
        self.groups = student_groups
        self.rooms = rooms
        self.working_days = working_days
        self.slots_per_day = (hours_per_day // lecture_duration)
        self.lecture_duration = lecture_duration
        self.time_slots = [(day, slot) for day in self.working_days for slot in range(self.slots_per_day)]
        self.lecture_requests = []
        self.schedule = {}

    def generate_lecture_requests(self):
        self.lecture_requests.clear()
        for group in self.groups:
            for subject, props in self.subjects.items():
                for i in range(props['sessions_per_week']):
                    self.lecture_requests.append((subject, group, i))

    def is_conflict(self, subject, group, room, time_slot, current_schedule):
        teacher = self.subjects[subject]['teacher']
        for (subj, grp, idx), (day, slot, assigned_room) in current_schedule.items():
            if (day, slot) == time_slot:
                # Conflict if same group, same teacher, or same room at same time
                if grp == group or self.subjects[subj]['teacher'] == teacher or assigned_room == room:
                    return True
        return False

    def generate_schedule_greedy(self):
        self.generate_lecture_requests()
        current_schedule = {}

        for subject, group, session_index in self.lecture_requests:
            assigned = False
            for time_slot in self.time_slots:
                for room in self.rooms:
                    if not self.is_conflict(subject, group, room, time_slot, current_schedule):
                        current_schedule[(subject, group, session_index)] = (*time_slot, room)
                        assigned = True
                        break
                if assigned:
                    break
            if not assigned:
                self.schedule = {}
                return False
        self.schedule = current_schedule
        return True

    def generate_schedule(self):
        """Try greedy, then fall back to backtracking if needed."""
        if self.generate_schedule_greedy():
            return True
        return self.generate_schedule_backtracking()

    def generate_schedule_backtracking(self):
        self.generate_lecture_requests()
        self.schedule = {}
        return self.backtrack(0, {})

    def backtrack(self, index, current_schedule):
        if index == len(self.lecture_requests):
            self.schedule = current_schedule.copy()
            return True

        subject, group, session_index = self.lecture_requests[index]
        for time_slot in self.time_slots:
            for room in self.rooms:
                if not self.is_conflict(subject, group, room, time_slot, current_schedule):
                    current_schedule[(subject, group, session_index)] = (*time_slot, room)
                    if self.backtrack(index + 1, current_schedule):
                        return True
                    del current_schedule[(subject, group, session_index)]
        return False

    def export_to_csv(self, filename="static/generated_schedule.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'Slot', 'Group', 'Subject', 'Teacher', 'Room', 'Session'])
            for (subject, group, session_index), (day, slot, room) in sorted(self.schedule.items(), key=lambda x: (x[1][0], x[1][1])):
                teacher = self.subjects[subject]['teacher']
                writer.writerow([day, f"Slot {slot + 1}", group, subject, teacher, room, session_index + 1])
