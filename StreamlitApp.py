import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st 
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging



#loading json file
with open("E:\Study Material\AIML-Subject\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQ Generator")

#create a form using st.form
with st.form("my_form"):
    #file uplaod
    uploaded_file = st.file_uploader("Upload a file")

    #input fields
    mcq_count = st.number_input("Enter the number of MCQs to generate", min_value=1, max_value=50, value=5)

    #subject
    subject = st.text_input("Insert Subjects",max_chars=20)

    #quiz tone
    tone = st.text_input("Enter complexity of questions",max_chars=20,placeholder="Simple")

    #ad button
    button = st.form_submit_button("Generate MCQs")
    #check if button is clickec and fields have input
    if button and file and mcq_count and subject and tone:
        with st.spinner("loading...."):
            try:
                text=read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": RESPONSE_JSON,
                        }
                    )
                    #st.write(response)

            except Exception as e:
                    traceback.print_exception(type(e),e,e.__traceback__)
                    st.error("Error")
            else:
                    print(f"Total Tokens: {cb.total_tokes}")
                    print(f"Prompt Tokens: {cb.promt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Total Cost: {cb.total_cost}")

                    if isinstance(response, dict):
                        quiz = response.get("quiz", None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.text_area(label="Review", value=response["review"])
                            else:
                                st.error("Error in the table data")
                    else:
                        st.write(response)



