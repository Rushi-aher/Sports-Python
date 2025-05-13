import streamlit as st
import sqlite3
from datetime import date

def insert_student_data(student_code, height, weight, arm_length, leg_length, wingspan, body_fat, grip_strength, vertical_jump, bench_press, deadlift, squat, heart_rate_resting, heart_rate_max, beep_test, yo_yo_test, shuttle_run_score, sprint_100m, shuttle_run_time, t_test_agility, hexagon_test, vertical_jump_explosiveness):
    conn = sqlite3.connect('student_athletes.db')
    cursor = conn.cursor()
    
    # Insert data into the student_measurements table
    cursor.execute("""
        INSERT INTO student_measurements 
        (student_code, height, weight, arm_length, leg_length, wingspan, body_fat, grip_strength, vertical_jump, bench_press, deadlift, squat, heart_rate_resting, heart_rate_max, beep_test, yo_yo_test, shuttle_run_score, sprint_100m, shuttle_run_time, t_test_agility, hexagon_test, vertical_jump_explosiveness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_code, height, weight, arm_length, leg_length, wingspan, body_fat, grip_strength, vertical_jump, bench_press, deadlift, squat, heart_rate_resting, heart_rate_max, beep_test, yo_yo_test, shuttle_run_score, sprint_100m, shuttle_run_time, t_test_agility, hexagon_test, vertical_jump_explosiveness))
    
    # Insert data into the progress_logs table
    cursor.execute("""
        INSERT INTO progress_logs (player_code, date, bench_press, squat, deadlift, sprint_100m, heart_rate_resting)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_code, date.today(), bench_press, squat, deadlift, sprint_100m, heart_rate_resting))
    
    conn.commit()
    conn.close()

def new_record_page():
    st.title("Enter New Student Data")
    
    student_code = st.text_input("Student Code")
    
    # Tabs for different types of measurements
    tab1, tab2, tab3, tab4 = st.tabs(["Physical Measurements", "Strength", "Cardiovascular Fitness", "Speed & Agility"])

    # Tab 1: Physical Measurements
    with tab1:
        st.header("Physical Measurements")
        height = st.number_input("Height (cm)", min_value=0, max_value=300, key="height")
        weight = st.number_input("Weight (kg)", min_value=0, max_value=300, key="weight")
        arm_length = st.number_input("Arm Length (cm)", min_value=0, max_value=150, key="arm_length")
        leg_length = st.number_input("Leg Length (cm)", min_value=0, max_value=150, key="leg_length")
        wingspan = st.number_input("Wingspan (cm)", min_value=0, max_value=300, key="wingspan")
        body_fat = st.number_input("Body Fat Percentage (%)", min_value=0.0, max_value=100.0, key="body_fat")

    # Tab 2: Strength Measurements
    with tab2:
        st.header("Strength Measurements")
        grip_strength = st.number_input("Grip Strength (kg)", min_value=0.0, max_value=100.0, key="grip_strength")
        vertical_jump = st.number_input("Vertical Jump (cm)", min_value=0.0, max_value=150.0, key="vertical_jump_strength")
        bench_press = st.number_input("Bench Press (kg)", min_value=0.0, max_value=300.0, key="bench_press")
        deadlift = st.number_input("Deadlift (kg)", min_value=0.0, max_value=500.0, key="deadlift")
        squat = st.number_input("Squat (kg)", min_value=0.0, max_value=500.0, key="squat")

    # Tab 3: Cardiovascular Fitness
    with tab3:
        st.header("Cardiovascular Fitness")
        heart_rate_resting = st.number_input("Heart Rate Resting (bpm)", min_value=30, max_value=200, key="heart_rate_resting")
        heart_rate_max = st.number_input("Heart Rate Max (bpm)", min_value=30, max_value=220, key="heart_rate_max")
        beep_test = st.number_input("Beep Test Level", min_value=0.0, max_value=20.0, key="beep_test")
        yo_yo_test = st.number_input("Yo-Yo Test Score", min_value=0, max_value=2000, key="yo_yo_test")
        shuttle_run_score = st.number_input("20m Shuttle Run Score", min_value=0, max_value=100, key="shuttle_run_score")

    # Tab 4: Speed, Agility & Explosiveness
    with tab4:
        st.header("Speed, Agility & Explosiveness")
        sprint_100m = st.number_input("100m Sprint (sec)", min_value=0.0, max_value=20.0, key="sprint_100m")
        shuttle_run_time = st.number_input("20m Shuttle Run Time (sec)", min_value=0.0, max_value=20.0, key="shuttle_run_time")
        t_test_agility = st.number_input("T-Test Agility (sec)", min_value=0.0, max_value=20.0, key="t_test_agility")
        hexagon_test = st.number_input("Hexagon Test (sec)", min_value=0.0, max_value=30.0, key="hexagon_test")
        vertical_jump_explosiveness = st.number_input("Vertical Jump (cm)", min_value=0.0, max_value=150.0, key="vertical_jump_explosiveness")

    # Submit button
    if st.button("Submit", key="submit"):
        insert_student_data(student_code, height, weight, arm_length, leg_length, wingspan, body_fat, grip_strength, vertical_jump, bench_press, deadlift, squat, heart_rate_resting, heart_rate_max, beep_test, yo_yo_test, shuttle_run_score, sprint_100m, shuttle_run_time, t_test_agility, hexagon_test, vertical_jump_explosiveness)
        st.success("Data Submitted Successfully!")
