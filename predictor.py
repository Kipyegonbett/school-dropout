import streamlit as st
import sqlite3
import pandas as pd

# Database file name
DATABASE_FILE = 'new.db'

# Initialize database and create table
def initialize_database():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            school_satisfaction FLOAT,
            attendance_rate FLOAT,
            failed_courses INTEGER,
            commute_time INTEGER,
            disciplinary_incidents INTEGER,
            homework_completion FLOAT,
            family_income TEXT,
            promotion_status TEXT
        );
        ''')
        conn.commit()

# Prediction logic
def predict_promotion(satisfaction, attendance, failed_courses, commute, disciplinary, homework, income):
    if (satisfaction > 3 and attendance > 70 and failed_courses <= 2 and
        commute <= 40 and disciplinary <= 2 and homework > 80 and
        income in ["low", "medium", "high"]):
        return "Promoted"
    else:
        return "Dropped Out"

# Insert student record
def insert_into_db(student_id, satisfaction, attendance, failed_courses, commute, disciplinary, homework, family_income, promotion_status):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO students (
                student_id, school_satisfaction, attendance_rate, failed_courses,
                commute_time, disciplinary_incidents, homework_completion,
                family_income, promotion_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, satisfaction, attendance, failed_courses, commute,
                  disciplinary, homework, family_income, promotion_status))
            conn.commit()
        return "Data inserted successfully!"
    except sqlite3.IntegrityError:
        return "Student ID already exists!"

# Fetch all records
def retrieve_data():
    with sqlite3.connect(DATABASE_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM students", conn)
    return df

# App UI using Streamlit
def main():
    st.set_page_config(page_title="Student Dropout Predictor", layout="centered")
    st.title("🎓 Student Dropout Predictor")

    st.markdown("Enter the student details below to predict if the student will be **Promoted** or **Dropped Out**.")

    with st.form("prediction_form"):
        student_id = st.number_input("Student ID", min_value=1, step=1)
        satisfaction = st.slider("School Satisfaction (1-5)", 1.0, 5.0, 3.0)
        attendance = st.slider("Attendance Rate (%)", 1.0, 100.0, 75.0)
        failed_courses = st.number_input("Failed Courses (0-10)", min_value=0, max_value=10, step=1)
        commute = st.slider("Commute Time (min)", 1, 120, 30)
        disciplinary = st.number_input("Disciplinary Cases", min_value=0, max_value=10, step=1)
        homework = st.slider("Homework Completion (%)", 0.0, 100.0, 85.0)
        family_income = st.selectbox("Family Income", ["low", "medium", "high"])

        submitted = st.form_submit_button("Predict and Insert")
        if submitted:
            try:
                promotion_status = predict_promotion(satisfaction, attendance, failed_courses, commute, disciplinary, homework, family_income)
                result = insert_into_db(student_id, satisfaction, attendance, failed_courses, commute, disciplinary, homework, family_income, promotion_status)
                st.success(f"Prediction: **{promotion_status}**")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")

    if st.button("📋 View Database Records"):
        df = retrieve_data()
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No records found.")

# Initialize DB and run the app
if __name__ == "__main__":
    initialize_database()
    main()
