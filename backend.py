import sqlite3
import hashlib

# Initialize and Connect to Database
def init_db():
    conn = sqlite3.connect("student_athletes.db")
    conn.close()

def connect_db():
    conn = sqlite3.connect('student_athletes.db')
    return conn

# Hashing Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create the new tables according to the updated schema
def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Create users table for login
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')

    # Create the new student_profiles table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            student_code INTEGER PRIMARY KEY,
            name TEXT,
            grade TEXT,
            university TEXT,
            sport TEXT,
            sex TEXT,
            contact TEXT
        )
    ''')

    # Create the new student_measurements table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_measurements (
            student_code INTEGER,
            height REAL,
            weight REAL,
            arm_length REAL,
            leg_length REAL,
            wingspan REAL,
            body_fat REAL,
            grip_strength REAL,
            vertical_jump REAL,
            bench_press REAL,
            deadlift REAL,
            squat REAL,
            heart_rate_resting INTEGER,
            heart_rate_max INTEGER,
            beep_test REAL,
            yo_yo_test REAL,
            shuttle_run_score REAL,
            sprint_100m REAL,
            shuttle_run_time REAL,
            t_test_agility REAL,
            hexagon_test REAL,
            vertical_jump_explosiveness REAL,
            FOREIGN KEY (student_code) REFERENCES student_profiles(student_code)
        )
    ''')

    # Create progress_logs table to track performance over time
    cur.execute('''
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_code INTEGER,
            date TEXT,
            bench_press INTEGER,
            squat INTEGER,
            deadlift INTEGER,
            sprint_100m_time REAL,
            resting_heart_rate INTEGER,
            FOREIGN KEY (player_code) REFERENCES student_profiles (student_code)
        )
    ''')

    conn.commit()
    conn.close()

# Registration Function
def register_user(username, name, email, password):
    hashed_password = hash_password(password)
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, name, email, hashed_password) VALUES (?, ?, ?, ?)',
                       (username, name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

# Authenticate Function
def authenticate_user(email, password):
    hashed_password = hash_password(password)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND hashed_password=?", (email, hashed_password))
    user = cur.fetchone()
    conn.close()
    return user

# Load student profile
def load_student_profile(student_code):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student_profiles WHERE student_code=?", (student_code,))
    profile = cur.fetchone()
    conn.close()

    if profile:
        profile_data = {
            "student_code": profile[0],
            "name": profile[1],
            "grade": profile[2],
            "university": profile[3],
            "sport": profile[4],
            "sex": profile[5],
            "contact": profile[6]
        }
        return profile_data
    return None

def load_student_measurements(student_code):
    conn = sqlite3.connect('student_athletes.db')
    cursor = conn.cursor()

    # Query to fetch student's measurements
    cursor.execute("""
        SELECT height, weight, arm_length, leg_length, wingspan, body_fat, 
               grip_strength, vertical_jump, heart_rate_resting, heart_rate_max,
               vertical_jump_explosiveness
        FROM student_measurements
        WHERE student_code = ?
    """, (student_code,))
    
    result = cursor.fetchone()
    conn.close()

    # Convert to a dictionary for easier access
    if result:
        return {
            'height': result[0],
            'weight': result[1],
            'arm_length': result[2],
            'leg_length': result[3],
            'wingspan': result[4],
            'body_fat': result[5],
            'grip_strength': result[6],
            'vertical_jump': result[7],
            'heart_rate_resting': result[8],
            'heart_rate_max': result[9],
            'vertical_jump_explosiveness': result[10],
        }
    return None  # Return None if no data found

# Save or update student measurements
def save_student_measurements(student_code, measurements):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT student_code FROM student_measurements WHERE student_code=?", (student_code,))
    exists = cur.fetchone()

    if exists:
        cur.execute('''
            UPDATE student_measurements
            SET height=?, weight=?, arm_length=?, leg_length=?, wingspan=?, body_fat=?, 
                grip_strength=?, vertical_jump=?, bench_press=?, deadlift=?, squat=?, 
                heart_rate_resting=?, heart_rate_max=?, beep_test=?, yo_yo_test=?, 
                shuttle_run_score=?, sprint_100m=?, shuttle_run_time=?, t_test_agility=?, 
                hexagon_test=?, vertical_jump_explosiveness=?
            WHERE student_code=?
        ''', (*measurements.values(), student_code))
    else:
        cur.execute('''
            INSERT INTO student_measurements (
                student_code, height, weight, arm_length, leg_length, wingspan, body_fat, 
                grip_strength, vertical_jump, bench_press, deadlift, squat, heart_rate_resting, 
                heart_rate_max, beep_test, yo_yo_test, shuttle_run_score, sprint_100m, 
                shuttle_run_time, t_test_agility, hexagon_test, vertical_jump_explosiveness
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_code, *measurements.values()))

    conn.commit()
    conn.close()


def update_student_profile(student_code, name, grade, university, sport, sex, contact):
    conn = sqlite3.connect('student_athletes.db')
    cursor = conn.cursor()
    
    # Update the student profile in the database
    cursor.execute("""
        UPDATE students
        SET name = ?, grade = ?, university = ?, sport = ?, sex = ?, contact = ?
        WHERE student_code = ?
    """, (name, grade, university, sport, sex, contact, student_code))
    
    conn.commit()
    conn.close()

# Create the tables on first run
if __name__ == "__main__":
    init_db()
    create_tables()
