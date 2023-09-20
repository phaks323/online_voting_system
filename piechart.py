import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

# Database connection parameters (replace with your own)
db_params = {
    'host': 'localhost',
    'port': 5430,
    'database': 'food_ordering_system',
    'user': 'postgres',
}

# Create a Streamlit app
st.title("Party Votes Distribution by Province")

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query to retrieve data (with casting to INTEGER and handling missing values)
    query = """
        SELECT province, SUM(CASE WHEN election_type ~ E'^\\d+$' THEN CAST(COALESCE(election_type, '0') AS INTEGER) ELSE 0 END) AS total_votes
        FROM votings_info
        GROUP BY province
    """

    # Execute the query
    cursor.execute(query)

    # Fetch data into a Pandas DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=['province', 'vote_count'])

    # Close the database connection
    conn.close()

    # Create a pie chart using Matplotlib
    fig, ax = plt.subplots()
    labels = df['province']
    sizes = df['vote_count']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart using Streamlit
    st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred: {e}")
