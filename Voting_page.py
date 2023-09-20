import psycopg2
import streamlit as st
from datetime import datetime
import subprocess

parties = [
    {
        "name": "African National Congress",
        "president": "Cyril Ramaphosa",
        "logo": "/Users/da_mac_41_/Downloads/African_National_Congress_logo.svg.png",
        "age": 68,
        "education": "LLB, University of South Africa",
    },
    {
        "name": "Democratic Alliance",
        "president": "John Steenhuisen",
        "logo": "/Users/da_mac_41_/Downloads/DA-logo.png",
        "age": 46,
        "education": "BA (Hons), University of Pretoria",
    },
    {
        "name": "Economic Freedom Fighters",
        "president": "Julius Malema",
        "logo": "/Users/da_mac_41_/Downloads/EFF_log.png",
        "age": 40,
        "education": "No formal tertiary qualification",
    },
    {
        "name": "Congress of the People (COPE)",
        "president": "Mosiuoa Lekota",
        "logo": "/Users/da_mac_41_/Downloads/COPE_logo.png",
        "age": 73,
        "education": "LLB, University of the North",
    },
    {
        "name": "United Democratic Movement (UDM)",
        "president": "Bantu Holomisa",
        "logo": "/Users/da_mac_41_/Downloads/UDM_logo.png",
        "age": 66,
        "education": "BA, University of Transkei",
    },
    {
        "name": "Inkatha Freedom Party (IFP)",
        "president": "Mangosuthu Buthelezi",
        "logo": "/Users/da_mac_41_/Downloads/IFP_logo.png",
        "age": 93,
        "education": "BA, University of Fort Hare",
    },
    {
        "name": "African Transformation Movement (ATM)",
        "president": "Vuyolwethu Zungula",
        "logo": "/Users/da_mac_41_/Downloads/ATM_logo.png",
        "age": 35,
        "education": "LLB, University of South Africa",
    },
    {
        "name": "Pan Africanist Congress (PAC)",
        "president": "Narius Moloto",
        "logo": "/Users/da_mac_41_/Downloads/PAC_logo.png",
        "age": 62,
        "education": "LLB, University of South Africa",
    },
]

# def voting_page():
#     st.title("Vote for your Favorite Party")
#     election_page()
#     # Create two columns
#     col1, col2 = st.columns(2)

#     # Display the radio buttons in each column
#     with col1:
#         selected_party_name_col1 = st.radio("Select Party", ["None"] + [party["name"] for party in parties[:len(parties)//2]])

#     with col2:
#         selected_party_name_col2 = st.radio("", ["None"] + [party["name"] for party in parties[len(parties)//2:]])

#     selected_party_name = selected_party_name_col1 if selected_party_name_col1 != "None" else selected_party_name_col2

#     if selected_party_name != "None":
#         selected_party = next((p for p in parties if p["name"] == selected_party_name), None)

#         # Display party information
#         st.subheader(selected_party["name"])
#         st.image(selected_party["logo"], caption=selected_party["name"], width=100)
#         st.write(f"President: {selected_party['president']}")
#         st.write(f"Age: {selected_party['age']}")
#         st.write(f"Educational Background: {selected_party['education']}")

#         # Create a checkbox to confirm the vote
#         vote_confirmed = st.checkbox(f"I confirm my vote for {selected_party['name']}")

#         # Create a submit button
#         submit_button = st.button("Submit Vote")

#         if vote_confirmed and submit_button:
#             # Add your logic to save the vote to the database or backend here
#             st.success(f"You voted for {selected_party['name']}!")

conn = psycopg2.connect(
    host="localhost",
    port=5430,
    database="food_ordering_system",
    user="postgres",

)


# Create a cursor object
cursor = conn.cursor()

# # Create a table for storing user information
# create_table_query = '''
#     CREATE TABLE IF NOT EXISTS user_info (
#         user_id SERIAL PRIMARY KEY,
#         hour TIMESTAMP,
#         dates DATE,
#         province VARCHAR(250),
#         party_name VARCHAR(250),
#         election_type VARCHAR(250)
        
        
        
#     )
# '''
# cursor.execute(create_table_query)
# conn.commit()

##from datetime import datetime
def voting_page(parties):
    st.title("Vote for your Favorite Party")

    # Get the selected election type from the Election Page
    election_type = st.selectbox("Select Election Type", ["National", "Local"])

    if election_type == "National":
        st.header("National Elections")
        # Include national election results here
    else:
        st.header("Local Elections")
        
    province_type = st.selectbox("Select Province", ["Eastern Cape", "Free State", "Gauteng","Kwazulu-Natal", "Limpopo","Mpumalanga","North West","Northern Cape","Western Cape"])


    col1, col2 = st.columns(2)

    # Display the radio buttons in each column
    with col1:
        selected_party_name_col1 = st.radio("Select Party", [party["name"] for party in parties[:len(parties)]])

    selected_party_name = selected_party_name_col1
    if selected_party_name != "None":
        selected_party = next((p for p in parties if p["name"] == selected_party_name), None)

        # Display party information
        st.subheader(selected_party["name"])
        st.image(selected_party["logo"], caption=selected_party["name"], width=100)
        st.write(f"President: {selected_party['president']}")
        st.write(f"Age: {selected_party['age']}")
        st.write(f"Educational Background: {selected_party['education']}")

        # Create a checkbox to confirm the vote
        vote_confirmed = st.checkbox(f"I confirm my vote for {selected_party['name']}")

        # Create a submit button
        submit_button = st.button("Submit Vote")

        if vote_confirmed and submit_button:
            # Add your logic to save the vote to the database or backend here

            # Get the current date and time
            hour = datetime.now()
            dates = datetime.now().date()

            # Insert the vote information into the database
            insert_vote_query = '''
                INSERT INTO votings_info (hour, dates,province,party_name,election_type)
                VALUES (%s,%s, %s,%s, %s)
            '''
            cursor.execute(insert_vote_query, (hour, dates,province_type,selected_party_name, election_type))
            conn.commit()

            st.success(f"You voted for {selected_party['name']}!")
            
        exit_button = st.button("Exit")
            
        if exit_button:
            subprocess.Popen(['streamlit', 'run', 'HomePage.py'])
 
voting_page(parties)
    # if selected_election_type:
    #     # Get the current date and time
    #     vote_time = datetime.now()
