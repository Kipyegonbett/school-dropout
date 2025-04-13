import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("student_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    school_satisfaction INTEGER,
    attendance_rate REAL,
    failed_courses INTEGER,
    commute_time INTEGER,
    disciplinary_cases INTEGER,
    homework_completion REAL,
    status TEXT
)
""")
conn.commit()

# Prediction function
def predict_promotion():
    try:
        # Gather data from input fields
        student_id = int(entry_student_id.get())  # New field for Student ID
        satisfaction = int(entry_satisfaction.get())
        attendance = float(entry_attendance.get())
        failed_courses = int(entry_failed_courses.get())
        commute_time = int(entry_commute_time.get())
        discipline = int(entry_disciplinary.get())
        homework = float(entry_homework.get())

        # Validate inputs
        if student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        if not (1 <= satisfaction <= 5):
            raise ValueError("School satisfaction must be between 1 and 5.")
        if not (0 <= attendance <= 100):
            raise ValueError("Attendance rate must be between 0 and 100%.")
        if not (0 <= failed_courses <= 10):
            raise ValueError("Failed courses must be between 0 and 10.")
        if not (0 <= commute_time <= 120):
            raise ValueError("Commute time must be between 0 and 120 minutes.")
        if not (0 <= discipline <= 10):
            raise ValueError("Disciplinary cases must be between 0 and 10.")
        if not (0 <= homework <= 100):
            raise ValueError("Homework completion must be between 0 and 100%.")

        # Determine promotion status
        reasons = []
        if satisfaction < 3:
            reasons.append("Low school satisfaction")
        if attendance < 70:
            reasons.append("Low attendance rate")
        if failed_courses > 2:
            reasons.append("Too many failed courses")
        if commute_time > 40:
            reasons.append("Long commute time")
        if discipline > 2:
            reasons.append("High disciplinary cases")
        if homework < 85:
            reasons.append("Low homework completion")

        if reasons:
            status = "Dropped Out"
            reason_text = ", ".join(reasons)
        else:
            status = "Promoted"
            reason_text = "N/A"

        # Show prediction result
        messagebox.showinfo("Prediction Result", f"Student ID: {student_id}\nStatus: {status}\nReason: {reason_text}")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Insert data into database
def insert_data():
    try:
        # Gather data from input fields
        student_id = int(entry_student_id.get())
        satisfaction = int(entry_satisfaction.get())
        attendance = float(entry_attendance.get())
        failed_courses = int(entry_failed_courses.get())
        commute_time = int(entry_commute_time.get())
        discipline = int(entry_disciplinary.get())
        homework = float(entry_homework.get())

        # Validate inputs
        if student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        if not (1 <= satisfaction <= 5):
            raise ValueError("School satisfaction must be between 1 and 5.")
        if not (0 <= attendance <= 100):
            raise ValueError("Attendance rate must be between 0 and 100%.")
        if not (0 <= failed_courses <= 10):
            raise ValueError("Failed courses must be between 0 and 10.")
        if not (0 <= commute_time <= 120):
            raise ValueError("Commute time must be between 0 and 120 minutes.")
        if not (0 <= discipline <= 10):
            raise ValueError("Disciplinary cases must be between 0 and 10.")
        if not (0 <= homework <= 100):
            raise ValueError("Homework completion must be between 0 and 100%.")

        # Determine promotion status
        reasons = []
        if satisfaction < 3:
            reasons.append("Low school satisfaction")
        if attendance < 70:
            reasons.append("Low attendance rate")
        if failed_courses > 2:
            reasons.append("Too many failed courses")
        if commute_time > 40:
            reasons.append("Long commute time")
        if discipline > 2:
            reasons.append("High disciplinary cases")
        if homework < 85:
            reasons.append("Low homework completion")

        if reasons:
            status = "Dropped Out"
        else:
            status = "Promoted"

        # Insert into the database
        cursor.execute(
            "INSERT INTO students (student_id, school_satisfaction, attendance_rate, failed_courses, commute_time, disciplinary_cases, homework_completion, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (student_id, satisfaction, attendance, failed_courses, commute_time, discipline, homework, status)
        )
        conn.commit()
        messagebox.showinfo("Success", "Data inserted into the database successfully!")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to insert data: {e}")

# Clear input fields
def clear_fields():
    entry_student_id.delete(0, tk.END)
    entry_satisfaction.delete(0, tk.END)
    entry_attendance.delete(0, tk.END)
    entry_failed_courses.delete(0, tk.END)
    entry_commute_time.delete(0, tk.END)
    entry_disciplinary.delete(0, tk.END)
    entry_homework.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Dropout Prediction and Data Entry")

# Input Fields
fields = [
    ("Student ID", "entry_student_id"),  # Added Student ID
    ("School Satisfaction (1-5)", "entry_satisfaction"),
    ("Attendance Rate (0-100)", "entry_attendance"),
    ("Failed Courses (1-10)", "entry_failed_courses"),
    ("Commute Time (0-120)", "entry_commute_time"),
    ("Disciplinary Cases (0-10)", "entry_disciplinary"),
    ("Homework Completion (0-100)", "entry_homework")
]

entries = {}

for idx, (label, var_name) in enumerate(fields):
    tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
    entries[var_name] = tk.Entry(root)
    entries[var_name].grid(row=idx, column=1, padx=10, pady=5)

# Unpacking entries for clarity
entry_student_id = entries["entry_student_id"]  # Added Student ID entry
entry_satisfaction = entries["entry_satisfaction"]
entry_attendance = entries["entry_attendance"]
entry_failed_courses = entries["entry_failed_courses"]
entry_commute_time = entries["entry_commute_time"]
entry_disciplinary = entries["entry_disciplinary"]
entry_homework = entries["entry_homework"]

# Buttons
btn_predict = tk.Button(root, text="Predict", command=predict_promotion)
btn_predict.grid(row=len(fields), column=0, padx=10, pady=10)

btn_clear = tk.Button(root, text="Clear", command=clear_fields)
btn_clear.grid(row=len(fields), column=2, padx=10, pady=10)

root.mainloop()
