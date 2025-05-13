import streamlit as st
import pandas as pd
import sqlite3

# Define the sports weightages (for demonstration purposes)
sports_attributes = pd.DataFrame({
    'Sport': ['Basketball', 'Soccer', 'Swimming'],
    'height': [0.3, 0.2, 0.1],
    'weight': [0.4, 0.3, 0.2],
    'arm_length': [0.3, 0.2, 0.1],
    'leg_length': [0.4, 0.3, 0.2],
    'wingspan': [0.5, 0.3, 0.1],
    'body_fat': [-0.1, -0.2, -0.3],
    'grip_strength': [0.4, 0.2, 0.1],
    'vertical_jump': [0.5, 0.3, 0.2],
    'heart_rate_resting': [-0.3, -0.2, -0.1],
    'heart_rate_max': [0.1, 0.1, 0.1],
    'vertical_jump_explosiveness': [0.6, 0.4, 0.3]
})

# Function to connect to the SQLite database and fetch student data by student_code
def get_student_data(student_code):
    conn = sqlite3.connect('student_athletes.db')
    query = f"SELECT * FROM student_measurements WHERE student_code = '{student_code}'"
    student_data = pd.read_sql(query, conn)
    conn.close()
    return student_data

# Prediction logic function
def predict_sport(student_row, sports_attributes):
    # Extract numeric physical attributes from the student row
    student_attributes = student_row[['height', 'weight', 'arm_length', 'leg_length', 'wingspan',
                                      'body_fat', 'grip_strength', 'vertical_jump', 'heart_rate_resting',
                                      'heart_rate_max', 'vertical_jump_explosiveness']].iloc[0]
    
    # Create an empty dictionary to store the scores for each sport
    sport_scores = {}
    
    # Calculate potential score for each sport by multiplying student attributes with sport weightages
    for i, sport_row in sports_attributes.iterrows():
        sport_name = sport_row['Sport']
        sport_weights = sport_row.drop('Sport')
        score = (student_attributes * sport_weights).sum()
        sport_scores[sport_name] = score
    
    # Find the sport with the highest score
    best_sport = max(sport_scores, key=sport_scores.get)
    
    return best_sport


def athlete_potential_page():
    # Streamlit App
    st.title("Sports Potential Predictor")

    # Input field for student code, stored in session_state to detect changes
    if 'student_code' not in st.session_state:
        st.session_state.student_code = ""

    student_code = st.text_input("Enter Student Code:", "")

    # Check if a new student code has been entered
    if student_code and student_code != st.session_state.student_code:
        st.session_state.student_code = student_code  # Update the session state with the new student code

        # Fetch student data from the database
        student_data = get_student_data(student_code)

        if not student_data.empty:
            st.write("Student Data:", student_data)

            # Predict the best sport for the student
            predicted_sport = predict_sport(student_data, sports_attributes)

            # Display the result
            st.success(f"The predicted best sport for student {student_code} is: {predicted_sport}")
        else:
            st.error("Student not found!")
    else:
        st.write("Enter a student code to see the results.")
