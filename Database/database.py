import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Abhas@12345',
    database='timetable'
)
cursor = conn.cursor()
def clear_cursor():
    try:
        cursor.fetchall()
    except:
        pass

def add_teacher(name):
    clear_cursor()
    cursor.execute("SELECT * FROM teachers WHERE name = %s", (name,))
    if cursor.fetchone():
        print(" Teacher already exists. Try a different name.")
    else:
        cursor.execute("INSERT INTO teachers (name) VALUES (%s)", (name,))
        conn.commit()
        print("Teacher added.")

def add_room(room_name):
    clear_cursor()
    cursor.execute("SELECT * FROM rooms WHERE room_name = %s", (room_name,))
    if cursor.fetchone():
        print(" Room already exists. Try a different name.")
    else:
        cursor.execute("INSERT INTO rooms (room_name) VALUES (%s)", (room_name,))
        conn.commit()
        print(" Room added.")

def add_subject(code, name):
    clear_cursor()
    cursor.execute("SELECT * FROM subjects WHERE Subcode = %s", (code,))
    if cursor.fetchone():
        print(" Subject code already exists. Try a different code.")
    else:
        cursor.execute("INSERT INTO subjects (Subcode, Subname) VALUES (%s, %s)", (code, name))
        conn.commit()
        print(" Subject added.")

def delTeacher(teacher_id):
    clear_cursor()
    cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
    conn.commit()
    print(" Teacher deleted.")

def delRoom(room_id):
    clear_cursor()
    cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
    conn.commit()
    print(" Room deleted.")

def delSub(subcode):
    clear_cursor()
    cursor.execute("DELETE FROM subjects WHERE Subcode = %s", (subcode,))
    conn.commit()
    print(" Subject deleted.")

def list_teachers():
    clear_cursor()
    cursor.execute("SELECT teacher_id, name FROM teachers")
    teachers = cursor.fetchall()
    if not teachers:
        print("No teachers found.")
    else:
        print("\nTeachers:")
        for tid, tname in teachers:
            print(f"ID: {tid} | Name: {tname}")

def list_rooms():
    clear_cursor()
    cursor.execute("SELECT room_id, room_name FROM rooms")
    rooms = cursor.fetchall()
    if not rooms:
        print("No rooms found.")
    else:
        print("\nRooms:")
        for rid, rname in rooms:
            print(f"ID: {rid} | Room Name: {rname}")

def list_subjects():
    clear_cursor()
    cursor.execute("SELECT Subcode, Subname FROM subjects")
    subjects = cursor.fetchall()
    if not subjects:
        print("No subjects found.")
    else:
        print("\nSubjects:")
        for code, name in subjects:
            print(f"Code: {code} | Name: {name}")

print("Welcome! Choose an option:")
while True:
    print("\nMain Menu:")
    print("1. Add")
    print("2. Delete")
    print("3. Display")
    print("4. Exit")
    main_choice = input("Enter choice: ")

    if main_choice == "1":
        while True:
            print("\nAdd Menu:")
            print("1. Add Teacher")
            print("2. Add Room")
            print("3. Add Subject")
            print("4. Back to Main Menu")
            add_choice = input("Enter choice: ")

            if add_choice == "1":
                teacher_name = input("Enter teacher name: ")
                add_teacher(teacher_name)
            elif add_choice == "2":
                room_name = input("Enter new room name: ")
                add_room(room_name)
            elif add_choice == "3":
                subject_code = input("Enter subject code: ")
                subject_name = input("Enter subject name: ")
                add_subject(subject_code, subject_name)
            elif add_choice == "4":
                break
            else:
                print("Invalid choice, try again.")

    elif main_choice == "2":
        
        while True:
            print("\nDelete Menu:")
            print("1. Delete Teacher")
            print("2. Delete Room")
            print("3. Delete Subject")
            print("4. Back to Main Menu")
            del_choice = input("Enter choice: ")

            if del_choice == "1":
                list_teachers()
                tid = input("Enter teacher_id to delete: ")
                delTeacher(tid)
            elif del_choice == "2":
                list_rooms()
                rid = input("Enter room_id to delete: ")
                delRoom(rid)
            elif del_choice == "3":
                list_subjects()
                subcode = input("Enter subject code to delete: ")
                delSub(subcode)
            elif del_choice == "4":
                break
            else:
                print("Invalid choice, try again.")

    elif main_choice == "3":
        print("\nDisplay Menu:")
        print("1. Show Teachers")
        print("2. Show Rooms")
        print("3. Show Subjects")
        print("4. Back to Main Menu")
        disp_choice = input("Enter choice: ")

        if disp_choice == "1":
            list_teachers()
        elif disp_choice == "2":
            list_rooms()
        elif disp_choice == "3":
            list_subjects()
        elif disp_choice == "4":
            continue
        else:
            print("Invalid choice, try again.")

    elif main_choice == "4":
        print("EXITING FROM THE DATABASE...!")
        break
    else:
        print("Invalid choice, please try again.")
