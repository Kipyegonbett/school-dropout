import streamlit as st
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("student_data.db", check_same_thread=False)
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

# --- Helper Function for Prediction ---
def predict_status(satisfaction, attendance, failed_courses, commute_time, discipline, homework):
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
        return "Dropped Out", reasons
    else:
        return "Promoted", ["N/A"]

# --- Streamlit UI ---
st.title("🎓 Student Dropout Prediction App")
st.write("Enter the student data below to predict promotion status and optionally save it to the database.")

# --- Input Form ---
with st.form("student_form"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    satisfaction = st.slider("School Satisfaction (1-5)", 1, 5)
    attendance = st.slider("Attendance Rate (%)", 0.0, 100.0)
    failed_courses = st.slider("Failed Courses", 0, 10)
    commute_time = st.slider("Commute Time (minutes)", 0, 120)
    discipline = st.slider("Disciplinary Cases", 0, 10)
    homework = st.slider("Homework Completion (%)", 0.0, 100.0)

    submitted = st.form_submit_button("Predict and Save")

# --- Prediction Logic ---
if submitted:
    status, reasons = predict_status(satisfaction, attendance, failed_courses, commute_time, discipline, homework)
    
    st.subheader("📊 Prediction Result")
    st.success(f"Status: {status}")
    st.info(f"Reason(s): {', '.join(reasons)}")

    # Save to Database
    try:
        cursor.execute(
            """
            INSERT INTO students (
                student_id, school_satisfaction, attendance_rate,
                failed_courses, commute_time, disciplinary_cases,
                homework_completion, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (student_id, satisfaction, attendance, failed_courses, commute_time, discipline, homework, status)
        )
        conn.commit()
        st.success("✅ Student data saved successfully!")
    except sqlite3.IntegrityError:
        st.error("❌ Student ID already exists. Please use a unique ID.")

# --- Optional: View Saved Data ---
if st.checkbox("📋 Show saved student data"):
    df = cursor.execute("SELECT * FROM students").fetchall()
    if df:
        import pandas as pd
        columns = ["ID", "Satisfaction", "Attendance", "Failed Courses", "Commute", "Disciplinary", "Homework", "Status"]
        st.dataframe(pd.DataFrame(df, columns=columns))
    else:
        st.info("No data found in the database yet.")
