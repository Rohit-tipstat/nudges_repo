import streamlit as st
from utils.data_analysis import analyze_student_exam_data
import pandas as pd
from helper_function.helper import remove_outliers_iqr_specific_columns
from utils.llm_response import custom_nudges
import time
import random


data = pd.read_csv("/home/ubuntu/student_loan_applications_with_branch.csv")
filtered_data = remove_outliers_iqr_specific_columns(data, ['Total COE'])


# Initialize required session state variables if they don't exist
if "source_city" not in st.session_state:
    st.session_state["source_city"] = ""

if "country_of_study" not in st.session_state:
    st.session_state["country_of_study"] = ""

if "university_name" not in st.session_state:
    st.session_state["university_name"] = ""

if "course_stream" not in st.session_state:
    st.session_state["course_stream"] = ""

if "current_city" not in st.session_state:
    st.session_state["current_city"] = ""

if "course_stream_selected" not in st.session_state:
    st.session_state["course_stream_selected"] = ""

# Access the session state variables safely
country_of_study = st.session_state["country_of_study"]
current_city = st.session_state["current_city"]
university_name = st.session_state["university_name"]
course_stream_selected = st.session_state["course_stream_selected"]


st.title("Personalized Nudges Based on Test taken")

# Options for the select box
test_options = ['GRE', 'IELTS', 'TOEFL', 'PTE']

test_selected = st.selectbox(
    "Select the country you want to study in:", test_options)

score_obtained = int(st.number_input("Enter the score"))
print("type(score_obtained)", type(score_obtained))

submit = st.button("Submit")
data_analysis_exam_score = analyze_student_exam_data(data=filtered_data, exam_taken=test_selected, score=score_obtained, course_type=course_stream_selected,
    source_city=current_city, country_selected=country_of_study, university_selected=university_name)


if submit:
    # Display the selections
    nudges_list = []
    start = time.time()
    # for result in data_analysis_exam_score:
    #     nudges_data = custom_nudges(result)
    #     print("nudges_data", nudges_data)
        
    #     # Extract and display only notifications from the custom nudges
    #     if nudges_data:
    #         for nudge in nudges_data:
    #             nudges_list.append(nudge.nudges)
    #         print("nudges_list--->", nudges_list)
            
    # # Display results cleanly
    # if nudges_list:
    #     st.write("### Personalized Nudges:")
    #     for nudge in nudges_list:
    #         for single_nudge in nudge:
    #             st.write(f"- {single_nudge}")
    # else:
    #     st.write("No nudges generated.")
    if data_analysis_exam_score:
        print("data_analysis_exam_score ", data_analysis_exam_score)
        random_result = random.choice(data_analysis_exam_score)
        print("Selected random result for nudge generation:", random_result)
        nudges_data = custom_nudges(random_result)
        print("Generated nudges data:", nudges_data)

        # Extract and display notifications
        if nudges_data:
            for nudge in nudges_data:
                nudges_list.append(nudge.nudges)

    # Display results cleanly
    if nudges_list:
        st.write("### Personalized Nudges:")
        for nudge in nudges_list:
            for single_nudge in nudge:
                st.write(f"- {single_nudge}")

    else:
        st.write("No nudges generated.")
    st.write("Time taken", time.time()-start)
