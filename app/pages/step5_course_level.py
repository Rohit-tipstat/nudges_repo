import streamlit as st
from utils.data_analysis import course_level_analysis
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

if "course_level_selected" not in st.session_state:
    st.session_state["course_level_selected"] = ""

# Access the session state variables safely
country_of_study = st.session_state["country_of_study"]
university_name = st.session_state["university_name"]
course_level_selected = st.session_state["course_level_selected"]
source_city = st.session_state['source_city']
st.title("Personalized Analysis Based on Course Level")

# Options for the select box
course_level_options = filtered_data['Course level'].dropna().unique().tolist()

course_level_selected = st.selectbox(
    "Select the Course Level:", course_level_options)

submit = st.button("Analyze")

data_analysis_course_level = course_level_analysis(
    data=filtered_data,
    course_level=course_level_selected,
    country_of_study=country_of_study,
    university_name=university_name,
    source_branch=source_city
)

if submit:
    nudges_list = []
    start = time.time()
    # for result in data_analysis_course_type:
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
    if data_analysis_course_level:
        print("data_analysis_course_level ", data_analysis_course_level)
        random_result = random.choice(data_analysis_course_level)
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
