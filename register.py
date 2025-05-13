import streamlit as st
from backend import register_user

# Registration function to be called in main app
def register():
    st.title("Register New User")
    with st.form("registration_form"):
        username = st.text_input("Username")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password == confirm_password:
            if st.form_submit_button("Register"):
                success = register_user(username, name, email, password)
                if success:
                    st.success("User registered successfully!")
                else:
                    st.error("Username already exists. Try another one.")
        else:
            st.error("Passwords do not match.")
