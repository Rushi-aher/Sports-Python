import streamlit as st
import streamlit_authenticator as stauth
from backend import load_credentials_from_db

# Login function to be called in main app
def login():
    # Load credentials from SQLite
    credentials = load_credentials_from_db()

    # Create the authenticator object
    authenticator = stauth.Authenticate(
        credentials['username'],
        'student_athlete_cookie',  # Cookie name
        'random_signature_key',    # Secret key for cookies
        30  # Cookie expiry in days
    )

    # Display login form and return values
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        st.write(f"Welcome {name}")
        st.title("Student Athlete Dashboard")
        return True, name  # User is authenticated
    elif authentication_status == False:
        st.error("Username/password is incorrect.")
    elif authentication_status == None:
        st.warning("Please enter your username and password.")

    return False, None  # Authentication failed or not attempted
