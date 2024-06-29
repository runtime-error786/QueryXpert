import sqlite3
import pandas as pd
import streamlit as st
from langchain_utils import run_llm_chain

def initialize_db():
    # Initialize the SQLite database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create the student table (for demonstration)
    c.execute('''CREATE TABLE IF NOT EXISTS student
                 (id INTEGER PRIMARY KEY, name TEXT, course_name TEXT)''')
    conn.commit()

    # Insert sample data (if table is empty)
    sample_data = [
        (1, 'John Doe', 'Math'),
        (2, 'Jane Smith', 'Math'),
        (3, 'Alice Johnson', 'Math'),
        (4, 'Bob Brown', 'Math'),
        (5, 'Charlie Davis', 'Art'),
        (6, 'Dana Wilson', 'Art'),
        (7, 'Eve Clark', 'Art'),
        (8, 'Frank White', 'Art'),
        (9, 'Grace Green', 'Biology'),
        (10, 'Hank Black', 'Biology')
    ]

    c.execute('SELECT COUNT(*) FROM student')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO student (id, name, course_name) VALUES (?, ?, ?)', sample_data)
        conn.commit()

    return conn

def execute_sql_query(user_text, conn):
    # Run language chain to get SQL query
    sql_query = run_llm_chain(user_text)

    if sql_query:
        # Print the SQL query for debugging
        st.info("Generated SQL Query:")
        st.code(sql_query, language='sql')

        try:
            # Execute the SQL query using pandas
            df = pd.read_sql_query(sql_query, conn)

            # Display results
            if not df.empty:
                st.success('Query Results:')
                st.write(df)
            else:
                st.warning("No results found.")
        except pd.DatabaseError as e:
            st.error(f"Pandas Database Error: {e}")
    else:
        st.error("No valid SQL query extracted.")
