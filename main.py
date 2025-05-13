import streamlit as st

# Set up main page layout and config (this must be the first Streamlit command)
st.set_page_config(
    page_title="Student Athlete Dashboard", 
    page_icon='📋',
    layout='wide',
    initial_sidebar_state='collapsed'
)


from pages import peer_comparison, user_profile, simulations
from backend import load_student_profile
from pages.athlete_potential import athlete_potential_page 
from pages.user_profile import user_profile_page
from pages.peer_comparison import peer_comparison_page
from pages.simulations import what_if_scenario_page
from pages.new_record import new_record_page
import streamlit_authenticator as stauth
#from backend import load_credentials_from_db




# Define pages
athlete_potential_page = st.Page(athlete_potential_page, title="Athlete Potential", icon="🏅")
user_profile_page = st.Page(user_profile_page, title="User Profile", icon="🚹")
peer_comparison_page = st.Page(peer_comparison_page, title="Peer Comparison", icon="📊")
simulations_page = st.Page(what_if_scenario_page, title="Simulations", icon="💻")
new_record_page = st.Page(new_record_page, title="New Record", icon="➕")


# Create navigation
pg = st.navigation([athlete_potential_page, peer_comparison_page, simulations_page, user_profile_page, new_record_page])
pg.run()




