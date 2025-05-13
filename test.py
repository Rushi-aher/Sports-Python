import sqlite3
from random import randint, uniform
from datetime import datetime, timedelta

# Connect to database
def connect_db():
    return sqlite3.connect('student_athletes.db')

# Function to generate sample progress logs
def generate_progress_logs(player_code, num_entries):
    conn = connect_db()
    
    for i in range(num_entries):
        date = datetime.now() - timedelta(days=i)
        bench_press = randint(50, 150)  # Random bench press weight
        squat = randint(60, 160)         # Random squat weight
        deadlift = randint(70, 170)      # Random deadlift weight
        sprint_100m_time = round(uniform(12.0, 15.0), 2)  # Random time in seconds
        resting_heart_rate = randint(60, 80)  # Random heart rate
        
        query = '''
            INSERT INTO progress_logs (player_code, date, bench_press, squat, deadlift, sprint_100m_time, resting_heart_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        conn.execute(query, (player_code, date.strftime('%Y-%m-%d'), bench_press, squat, deadlift, sprint_100m_time, resting_heart_rate))
    
    conn.commit()
    conn.close()

# Generate progress logs for P001 and P002
generate_progress_logs('P001', 20)
generate_progress_logs('P002', 20)

print("Progress logs generated for P001 and P002.")
