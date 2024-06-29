import streamlit as st
from langchain_utils import run_llm_chain
from sql_utils import initialize_db, execute_sql_query

# Initialize the SQLite database
conn = initialize_db()

# Custom CSS for Streamlit (can be imported from css_styles.css if needed)
custom_css = """
<style>
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f7f7f7;
    margin: 0;
    padding: 0;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin-top: 10px;
}

.stButton>button:hover {
    background-color: #45a049;
}

.stTextInput>div>div>input {
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 8px;
    font-size: 16px;
    width: 100%;
}

.stTextInput>label {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
}

.stMarkdown {
    margin-bottom: 20px;
}

.stSuccess {
    color: #4CAF50;
    font-weight: bold;
}

.stError {
    color: #FF5733;
    font-weight: bold;
}
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Define the Streamlit app
st.title('Text to SQL Converter')

# Display introductory text and instructions
st.markdown("""
            
            Enter a query in natural language to retrieve data from the student database.

            Example queries:
            - "Give total count of students who study Math"
            - "List names of students who study Biology"

            """)

# User input text area
user_text = st.text_area("Enter your query:")

# Convert and execute button
if st.button('Convert and Execute'):
    if user_text:
        # Run language chain and SQL query
        execute_sql_query(user_text, conn)

# Close the connection
conn.close()
