import streamlit as st
from backend import load_student_profile, update_student_profile  # Import function to load and update student data from the backend

def load_profile(student_code):
    # Simulate profile loading from database using the code
    profile_data = load_student_profile(student_code)
    return profile_data

def user_profile_page():
    st.title("Student Athlete Profile")
    
    # Load Profile Section
    if 'profile_loaded' not in st.session_state:
        st.session_state.profile_loaded = False
    
    if not st.session_state.profile_loaded:
        student_code = st.text_input("Enter Student Code to Load Profile")
        if st.button("Load Profile"):
            profile_data = load_profile(student_code)
            if profile_data:
                st.session_state.profile_loaded = True
                st.session_state.profile_data = profile_data
                st.success("Profile Loaded Successfully!")
            else:
                st.error("Invalid Student Code. Please try again.")
    
    # Once the profile is loaded
    if st.session_state.profile_loaded:
        profile_data = st.session_state.profile_data
        with st.container():
            st.subheader("Student Information")
            name = st.text_input("Name", value=profile_data['name'])
            grade = st.text_input("Grade", value=profile_data['grade'])
            university = st.text_input("University", value=profile_data['university'])
            sport = st.text_input("Sport", value=profile_data['sport'])
            sex = st.selectbox("Sex", ["Male", "Female"], index=0 if profile_data['sex'] == "Male" else 1)
            contact = st.text_input("Contact", value=profile_data['contact'])

            if st.button("Update Profile"):
                update_student_profile(student_code, name, grade, university, sport, sex, contact)
                st.success("Profile Updated Successfully!")

        # Option to go to the new record page
        if st.button("Enter New Data"):
            st.query_params(page="new_record")  # Redirect to new_record page
