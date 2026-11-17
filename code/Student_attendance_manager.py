"""
PS 14 - Student Attendance Manager
Course : Programming Fundamentals and Logic Building using Python
Concepts: Lists, Dictionaries, Functions, File Handling (+ try/except, f-strings)

Each student is a dictionary:
    {"roll": 101, "name": "Aman", "held": 4, "attended": 3}
All students are stored in a list and saved in attendance.txt
(one student per line:  roll,name,held,attended)
"""

FILE_NAME = "attendance.txt"
MIN_PERCENT = 75          # minimum required attendance


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------
def load_data():
    """Read attendance.txt and return a list of student dictionaries."""
    students = []
    try:
        file = open(FILE_NAME, "r")
        for line in file:
            line = line.strip()
            if line == "":
                continue                      # skip blank lines
            parts = line.split(",")
            if len(parts) != 4:
                continue                      # skip damaged lines
            student = {
                "roll": int(parts[0]),
                "name": parts[1],
                "held": int(parts[2]),
                "attended": int(parts[3]),
            }
            students.append(student)
        file.close()
    except FileNotFoundError:
        pass                                  # first run: no file yet
    except ValueError:
        print("Warning: attendance.txt has bad data. Some records skipped.")
    return students


def save_data(students):
    """Write the whole list back to attendance.txt (called after every change)."""
    file = open(FILE_NAME, "w")
    for s in students:
        file.write(f"{s['roll']},{s['name']},{s['held']},{s['attended']}\n")
    file.close()


# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------
def find_student(students, roll):
    """Return the student dictionary with this roll number, or None."""
    for s in students:
        if s["roll"] == roll:
            return s
    return None


def calc_percentage(student):
    """Attendance percentage. Avoids division by zero when held == 0."""
    if student["held"] == 0:
        return 0.0
    return student["attended"] / student["held"] * 100


def read_roll(message="Enter roll number: "):
    """Ask for a roll number; return int, or None if input is not a number."""
    text = input(message).strip()
    try:
        return int(text)
    except ValueError:
        print("Invalid roll number. Enter digits only.")
        return None


# ---------------------------------------------------------------
# Main features
# ---------------------------------------------------------------
def add_student(students):
    roll = read_roll()
    if roll is None:
        return
    if roll <= 0:
        print("Roll number must be positive.")
        return
    if find_student(students, roll) is not None:
        print(f"Roll number {roll} already exists.")
        return

    name = input("Enter name: ").strip()
    if name == "" or "," in name:
        print("Invalid name. It cannot be empty or contain a comma.")
        return

    student = {"roll": roll, "name": name, "held": 0, "attended": 0}
    students.append(student)
    save_data(students)
    print(f"Student added: {roll} | {name} | Held: 0 | Attended: 0")


def mark_attendance(students):
    roll = read_roll()
    if roll is None:
        return
    student = find_student(students, roll)
    if student is None:
        print(f"Roll number {roll} not found.")
        return

    status = input("Enter status (P/A): ").strip().upper()
    if status != "P" and status != "A":
        print("Invalid status. Enter P or A.")
        return

    student["held"] += 1
    if status == "P":
        student["attended"] += 1
    save_data(students)
    print(f"Marked {'Present' if status == 'P' else 'Absent'} for "
          f"{student['name']}. Held: {student['held']} | "
          f"Attended: {student['attended']}")


def show_percentage(students):
    roll = read_roll()
    if roll is None:
        return
    student = find_student(students, roll)
    if student is None:
        print(f"Roll number {roll} not found.")
        return

    percent = calc_percentage(student)
    if student["held"] == 0:
        print(f"{student['name']}: Attendance {percent:.2f}% (no classes held yet)")
    else:
        print(f"{student['name']}: Attendance {percent:.2f}%")


def shortage_list(students):
    if len(students) == 0:
        print("No students found.")
        return

    below = []
    ok = []
    for s in students:
        if calc_percentage(s) < MIN_PERCENT:
            below.append(s)
        else:
            ok.append(s)

    if len(below) > 0:
        print(f"Below {MIN_PERCENT}%:")
        for s in below:
            print(f"{s['roll']} | {s['name']} | {calc_percentage(s):.2f}%")
    else:
        print(f"No student is below {MIN_PERCENT}%.")

    for s in ok:
        print(f"{s['name']} ({calc_percentage(s):.2f}%) meets the requirement.")


def view_all(students):
    if len(students) == 0:
        print("No students found.")
        return
    print(f"{'Roll':<8}{'Name':<15}{'Held':<8}{'Attended':<10}{'Percent'}")
    print("-" * 50)
    for s in students:
        print(f"{s['roll']:<8}{s['name']:<15}{s['held']:<8}"
              f"{s['attended']:<10}{calc_percentage(s):.2f}%")


def show_menu():
    print("\n===== STUDENT ATTENDANCE MANAGER =====")
    print("1. Add student")
    print("2. Mark attendance (P/A)")
    print("3. Show attendance percentage")
    print("4. Shortage list (below 75%)")
    print("5. View all students")
    print("6. Exit")


# ---------------------------------------------------------------
# Program starts here
# ---------------------------------------------------------------
def main():
    students = load_data()          # load file at start

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            mark_attendance(students)
        elif choice == "3":
            show_percentage(students)
        elif choice == "4":
            shortage_list(students)
        elif choice == "5":
            view_all(students)
        elif choice == "6":
            save_data(students)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


main()