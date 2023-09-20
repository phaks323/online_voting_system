import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import psycopg2

def display_election_dashboard():
    # Function to fetch data from the database and create DataFrames
    def fetch_data(election_type):
        conn = psycopg2.connect(
            host="localhost",
            port=5430,  # Change the port if necessary
            database="food_ordering_system",
            user="postgres",
        )

        # Create a cursor
        cursor = conn.cursor()

        # Initialize variables to store counts for both local and national elections
        total_registered_voters = 0
        total_votes = 0
        party_votes_data = []

        # Fetch the count of registered voters from the user_info table for both local and national elections
        cursor.execute("SELECT COUNT(*) FROM user_info;")
        total_registered_voters = cursor.fetchone()[0]

        # Fetch the count of votes cast for both local and national elections from the voting_info table
        if election_type == "None":
            cursor.execute("SELECT COUNT(*) FROM votings_info;")
        else:
            cursor.execute("SELECT COUNT(*) FROM votings_info WHERE election_type = %s;", (election_type,))
        total_votes = cursor.fetchone()[0]

        # Fetch party names and their vote counts for both local and national elections from the voting_info table
        if election_type == "None":
            cursor.execute("SELECT party_name, COUNT(*) FROM votings_info GROUP BY party_name;")
        else:
            cursor.execute("SELECT party_name, COUNT(*) FROM votings_info WHERE election_type = %s GROUP BY party_name;", (election_type,))
        party_votes_data = cursor.fetchall()

        # Fetch province, party_name, and vote counts for both local and national elections from the voting_info table
        if election_type == "None":
            cursor.execute("SELECT province, party_name, COUNT(*) FROM votings_info GROUP BY province, party_name;")
        else:
            cursor.execute("SELECT province, party_name, COUNT(*) FROM votings_info WHERE election_type = %s GROUP BY province, party_name;", (election_type,))
        province_party_votes_data = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        # Create DataFrames
        party_results = pd.DataFrame(party_votes_data, columns=['Party', 'Votes'])
        province_party_results = pd.DataFrame(province_party_votes_data, columns=['Province', 'Party', 'Votes'])

        return total_registered_voters, total_votes, party_results, province_party_results, party_votes_data

    # Streamlit app title
    st.title("Election Dashboard")
    # Add a selector (dropdown) to switch between national, local, and both elections
    election_type = st.selectbox("Select Election Type", ["None", "National", "Local"])

    # Create a layout with three columns
    col1, col2, col3 = st.columns(3)

    # Display registered voters count in the first column
    with col1:
        total_registered_voters, total_votes, party_results, province_party_results, party_votes_data = fetch_data(election_type)
        st.subheader("Registered Voters")
        st.info(f"{total_registered_voters}")

    # Display votes cast count in the second column
    with col2:
        st.subheader("Votes Cast")
        st.info(f"{total_votes}")

    # Calculate and display the vote percentage in the third column
    with col3:
        st.subheader("Total Votes")
        vote_percentage = (total_votes / total_registered_voters) * 100
        st.info(f"{vote_percentage:.2f}%")

    # Create a bar chart for party-wise results using Altair
    col4, col5 = st.columns([1, 2])
    with col4:
        st.subheader("Party-wise Results")

        # Calculate vote percentages
        party_results['Vote Percentage'] = (party_results['Votes'] / total_votes) * 100

        # Create a bar chart for party-wise results using Altair
        chart = alt.Chart(party_results).mark_bar().encode(
            x='Party',
            y='Vote Percentage:Q'
        ).properties(
            width=400,
            height=300
        )

        st.altair_chart(chart)

    # Pivot the province-party results
    province_party_pivot = province_party_results.pivot(index='Party', columns='Province', values='Votes').fillna(0).astype(int)

    # Create a table for province-wise results
    st.header("Province-wise Results")
    st.table(province_party_pivot)
    
display_election_dashboard()
