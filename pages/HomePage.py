import streamlit as st
import subprocess
import os

def homepage():
    
    st.title("Welcome to VoteConnect!")
    # Add the logo at the top of the page
    st.image("/Users/da_mac_41_/Downloads/logs.png", caption="Every Vote Counts", width=200)


    st.markdown("## Introduction")
    st.write("The Online Voting System allows registered users to cast their votes "
             "in various elections securely and conveniently.")

    st.markdown("## Voter Registration")
    st.write("If you are a new user, you can register to vote in the upcoming elections.")
    register_button = st.button("Register Now")
    if register_button:
        # Redirect to the voter registration page
        st.write("Redirecting to the voter registration page...")
        subprocess.Popen(['streamlit', 'run', 'Register.py'])
        
        # Add your logic to redirect the user to the registration page

    st.markdown("## Already Have an Account?")
    st.write("If you already have an account, you can log in to access your voting dashboard.")
    login_link = st.button("Log In")
    if login_link:
        st.write('Redirecting to login page...')
        subprocess.Popen(['streamlit', 'run', 'LoginPage.py'])
        
        
        
        
        # Add your logic to redirect the user to the login page
homepage()