from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
import json
import streamlit as st

def run_llm_chain(user_text):
    # Initialize the LLM
    llm = Ollama(model='llama3')

    # Define the prompt template
    response = """{
        result : query
        }"""
    template = """
    You are an AI that converts natural language to SQL.only write the query which user want and search from table is not case sensitive
    Here is the schema of the table student:
    id: INTEGER, name: TEXT, course_name: TEXT
    only return json object like {response}
    Convert the following text to an SQL query:
    {text}
    """
    prompt = PromptTemplate(template=template, input_variables=["text","response"])

    # Create the LLMChain
    sql_chain = LLMChain(llm=llm, prompt=prompt)

    # Convert text to SQL
    result = sql_chain.run({"text": user_text,"response":response})

    # Check if result is a string
    if isinstance(result, str):
        # Attempt to extract JSON-like content
        try:
            # Extracting the query from the string
            query_start_index = result.find("{")
            query_end_index = result.rfind("}") + 1
            json_str = result[query_start_index:query_end_index]

            # Parsing the extracted JSON-like content
            result_json = json.loads(json_str)

            # Extract SQL query from JSON result
            sql_query = result_json.get("result")
            return sql_query
        except Exception as e:
            st.error(f"Error processing model output: {e}")
            return None
    else:
        st.error("Unexpected model output format.")
        return None
