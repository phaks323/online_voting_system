import streamlit as st
from Register import registration_page
from HomePage import homepage
from LoginPage import login_page
from Dashboard import display_election_dashboard

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", ("Home","Login", "Register","Vote","view"))
    
    if page == "Home":
        homepage()
        
    elif page == "Login":
        login_page()
        
    elif page == "Register":
        registration_page()
        
        
    # elif page == "Record":
    #     record_audio()
    
    # elif page == "Election":
    #     election_page()
    
    # elif page == "Vote":
    #     voting_page(parties)
    
    elif page == "view":   
         display_election_dashboard()
    
     

if __name__ == "__main__":
    main()