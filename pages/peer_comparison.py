import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Connect to database
def connect_db():
    return sqlite3.connect('student_athletes.db')

# Fetch individual athlete data by player code
def fetch_athlete_data(player_code):
    conn = connect_db()
    query = '''
        SELECT * FROM student_profiles
        JOIN student_measurements ON student_profiles.student_code = student_measurements.student_code
        WHERE student_profiles.student_code = ?
    '''
    player_data = pd.read_sql(query, conn, params=(player_code,))
    conn.close()
    return player_data

# Fetch progress logs for a specific player
def fetch_progress_logs(player_code):
    conn = connect_db()
    query = '''
        SELECT date, bench_press, squat, deadlift, sprint_100m, heart_rate_resting
        FROM progress_logs WHERE player_code = ?
    '''
    progress_data = pd.read_sql(query, conn, params=(player_code,))
    progress_data['date'] = pd.to_datetime(progress_data['date'])  # Ensure date is in datetime format
    conn.close()
    return progress_data

# Function to fetch and compare athlete data
def peer_comparison_page():
    st.title("Peer Comparison")

    # Input player codes
    player_code1 = st.text_input("Enter Player Code 1")
    player_code2 = st.text_input("Enter Player Code 2")

    if st.button("Compare"):
        if player_code1 == player_code2:
            st.error("Please enter two different player codes for comparison.")
            return

        player_data1 = fetch_athlete_data(player_code1)
        player_data2 = fetch_athlete_data(player_code2)

        if player_data1.empty or player_data2.empty:
            st.error("One or both players not found! Please enter valid player codes.")
        else:
            school = player_data1.iloc[0]['school']  # Assuming both players are from the same school

            # Create columns for side-by-side comparison
            col1, col2 = st.columns(2)

            # Metrics Display
            with col1:
                st.subheader(f"{player_data1.iloc[0]['name']} Metrics")
                st.metric(label="Bench Press", value=f"{player_data1.iloc[0]['bench_press']} kg")
                st.metric(label="Squat", value=f"{player_data1.iloc[0]['squat']} kg")
                st.metric(label="Deadlift", value=f"{player_data1.iloc[0]['deadlift']} kg")
                st.metric(label="Sprints 100m", value=f"{player_data1.iloc[0]['sprint_100m']} sec")
                st.metric(label="Resting Heart Rate", value=f"{player_data1.iloc[0]['heart_rate_resting']} bpm")

            with col2:
                st.subheader(f"{player_data2.iloc[0]['name']} Metrics")
                st.metric(label="Bench Press", value=f"{player_data2.iloc[0]['bench_press']} kg")
                st.metric(label="Squat", value=f"{player_data2.iloc[0]['squat']} kg")
                st.metric(label="Deadlift", value=f"{player_data2.iloc[0]['deadlift']} kg")
                st.metric(label="Sprints 100m", value=f"{player_data2.iloc[0]['sprint_100m']} sec")
                st.metric(label="Resting Heart Rate", value=f"{player_data2.iloc[0]['heart_rate_resting']} bpm")

            # Create tabs for different comparison categories
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Strength", "Speed & Agility", "Cardiovascular Fitness", 
                "Physical Measurements", "Progress Over Time"
            ])

            # Strength Comparison
            with tab1:
                st.subheader("Strength Comparison")
                strength_cols = ['bench_press', 'squat', 'deadlift']
                
                # Bar chart comparing both players
                combined_strength = pd.DataFrame({
                    'Player 1': player_data1[strength_cols].iloc[0],
                    'Player 2': player_data2[strength_cols].iloc[0]
                })
                st.bar_chart(combined_strength)

            # Speed & Agility Comparison
            with tab2:
                st.subheader("Speed & Agility Comparison")
                speed_cols = ['sprint_100m', 'shuttle_run_time', 't_test_agility', 'hexagon_test']
                
                # Check if columns exist
                available_speed_cols = [col for col in speed_cols if col in player_data1.columns]

                if available_speed_cols:
                    # Line chart comparing speed metrics
                    combined_speed = pd.DataFrame({
                        'Player 1': player_data1[available_speed_cols].iloc[0],
                        'Player 2': player_data2[available_speed_cols].iloc[0]
                    })
                    st.line_chart(combined_speed)
                else:
                    st.warning("No Speed & Agility metrics found for these players.")

            # Cardiovascular Fitness Comparison
            with tab3:
                st.subheader("Cardiovascular Fitness Comparison")
                cardio_cols = ['heart_rate_resting', 'beep_test', 'yo_yo_test']

                # Bar chart comparing cardiovascular fitness
                combined_cardio = pd.DataFrame({
                    'Player 1': player_data1[cardio_cols].iloc[0],
                    'Player 2': player_data2[cardio_cols].iloc[0]
                })
                st.bar_chart(combined_cardio)

            # Physical Measurements Comparison
            with tab4:
                st.subheader("Physical Measurements Comparison")
                physical_cols = ['height', 'weight', 'wingspan', 'body_fat']

                combined_physical = pd.DataFrame({
                    'Player 1': player_data1[physical_cols].iloc[0],
                    'Player 2': player_data2[physical_cols].iloc[0]
                })
                st.bar_chart(combined_physical)

            # Progress Over Time Comparison
            with tab5:
                st.subheader("Progress Over Time Comparison")
                
                # Fetching both players' progress
                progress_data1 = fetch_progress_logs(player_code1)
                progress_data2 = fetch_progress_logs(player_code2)

                if progress_data1.empty or progress_data2.empty:
                    st.write("No progress data available for one or both players.")
                else:
                    st.write("Player 1 Progress Over Time:")
                    st.line_chart(progress_data1.set_index('date')[['bench_press', 'squat', 'deadlift']].rolling(window=3).mean())
                    
                    st.write("Player 2 Progress Over Time:")
                    st.line_chart(progress_data2.set_index('date')[['bench_press', 'squat', 'deadlift']].rolling(window=3).mean())
                    
                    # Comparing their growth in metrics
                    combined_progress = pd.DataFrame({
                        'Player 1': progress_data1.set_index('date')[['bench_press', 'squat', 'deadlift']].mean(),
                        'Player 2': progress_data2.set_index('date')[['bench_press', 'squat', 'deadlift']].mean()
                    })
                    st.write("Average Progress Comparison:")
                    st.line_chart(combined_progress)
