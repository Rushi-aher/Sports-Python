import streamlit as st
import pandas as pd
from backend import load_student_measurements  # Import your function to load student measurements

# Weightage data
sports_weightages = pd.DataFrame({
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

def what_if_scenario_page():
    st.title("What If Scenario: Athlete Profile")
    # Input player codes
    student_code = st.text_input("Enter Player Code")

    # Load student measurements from the database
    student_profile = load_student_measurements(student_code)
    
    if student_profile is None:
        st.error("Student profile not found. Please check the student code.")
        return
    
    # Display student stats
    st.subheader("Your Current Stats")
    col1, col2,col3,col4 = st.columns(4)
    statlist = []
    vallist = []
    for stat, value in student_profile.items():
        statlist.append(stat)
        vallist.append(value)
            
    for i in range(0,3):
        col1.metric(label=statlist[i].capitalize(), value=vallist[i])

    for i in range(3,6):
        col2.metric(label=statlist[i].capitalize(), value=vallist[i])

    for i in range(6,9):
        col3.metric(label=statlist[i].capitalize(), value=vallist[i])

    for i in range(10,11):
        col4.metric(label=statlist[i].capitalize(), value=vallist[i])


    # Sports buttons
    for sport in sports_weightages['Sport']:
        if st.button(sport):
            st.session_state.selected_sport = sport
            st.success(f"You selected: {sport}")
            display_stats_for_sport(student_profile, sport)

def display_stats_for_sport(student_profile, sport):
    st.subheader(f"Suggested Changes for {sport}")
    
    sport_data = sports_weightages[sports_weightages['Sport'] == sport].iloc[0]
    
    for stat in sport_data.index[1:]:
        target_weightage = sport_data[stat]
        current_value = student_profile[stat]
        
        # Calculate the target value
        if target_weightage > 0:
            target_value = current_value + (current_value * target_weightage)
            delta = target_value - current_value
            color = "green"  # Positive change needed
        else:
            target_value = current_value + (current_value * target_weightage)
            delta = target_value - current_value
            color = "red"  # Negative change needed
            
        # Display the metric with delta
        st.markdown(f"<div style='color: {color};'>**{stat.capitalize()}:** {target_value:.2f} (Δ: {delta:.2f})</div>", unsafe_allow_html=True)

# Call the function with a student code (for testing purposes, replace with actual code)
# what_if_scenario('P001')  # Example student code
