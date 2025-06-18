# import csv

# class EnhancedScheduler:
#     def __init__(self, subjects, student_groups, rooms, working_days, hours_per_day, lecture_duration):
#         self.subjects = subjects
#         self.groups = student_groups
#         self.rooms = rooms
#         self.working_days = working_days
#         self.slots_per_day = hours_per_day // lecture_duration
#         self.break_after_slots = 2  # insert a break after every 2 lecture slots
#         self.time_slots = self.generate_valid_time_slots()
#         self.lecture_requests = []
#         self.schedule = {}

#     def generate_valid_time_slots(self):
#         valid_slots = []
#         for day in self.working_days:
#             for slot in range(self.slots_per_day):
#                 # Exclude break slots
#                 if (slot + 1) % (self.break_after_slots + 1) != 0:
#                     valid_slots.append((day, slot))
#         return valid_slots

#     def generate_lecture_requests(self):
#         self.lecture_requests = []
#         for group in self.groups:
#             for subject, props in self.subjects.items():
#                 for i in range(props['sessions_per_week']):
#                     self.lecture_requests.append((subject, group, i))

#     def is_conflict(self, subject, group, room, time_slot, current_schedule):
#         teacher = self.subjects[subject]['teacher']
#         for (subj, grp, idx), (day, slot, assigned_room) in current_schedule.items():
#             if (day, slot) == time_slot:
#                 if grp == group or self.subjects[subj]['teacher'] == teacher or assigned_room == room:
#                     return True
#         return False

#     def backtrack_schedule(self, index, current_schedule):
#         if index == len(self.lecture_requests):
#             return True  # All sessions scheduled

#         subject, group, session_index = self.lecture_requests[index]

#         for time_slot in self.time_slots:
#             for room in self.rooms:
#                 if not self.is_conflict(subject, group, room, time_slot, current_schedule):
#                     current_schedule[(subject, group, session_index)] = (*time_slot, room)
#                     if self.backtrack_schedule(index + 1, current_schedule):
#                         return True
#                     del current_schedule[(subject, group, session_index)]  # Backtrack

#         return False  # No valid slot found

#     def generate_schedule_greedy(self):
#         self.generate_lecture_requests()
#         current_schedule = {}

#         if self.backtrack_schedule(0, current_schedule):
#             self.schedule = current_schedule
#             return True
#         else:
#             self.schedule = {}
#             return False

#     def export_to_csv(self, filename="static/generated_schedule.csv"):
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Day', 'Slot', 'Group', 'Subject', 'Teacher', 'Room', 'Session'])
#             for (subject, group, session_index), (day, slot, room) in sorted(self.schedule.items(), key=lambda x: (x[1][0], x[1][1])):
#                 teacher = self.subjects[subject]['teacher']
#                 writer.writerow([day, f"Slot {slot + 1}", group, subject, teacher, room, session_index + 1])
