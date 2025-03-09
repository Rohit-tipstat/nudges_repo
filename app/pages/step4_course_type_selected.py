import streamlit as st
from utils.data_analysis import course_type_analysis
import pandas as pd
from helper_function.helper import remove_outliers_iqr_specific_columns
from utils.llm_response import custom_nudges
import time
import random

data = pd.read_csv("/home/ubuntu/student_loan_applications_with_branch.csv")
filtered_data = remove_outliers_iqr_specific_columns(data, ['Total COE'])


# Ensure required session variables are set
if "source_city" not in st.session_state:
    st.session_state["source_city"] = ""

if "country_of_study" not in st.session_state:
    st.session_state["country_of_study"] = ""

if "university_name" not in st.session_state:
    st.session_state["university_name"] = ""

if "course_stream" not in st.session_state:
    st.session_state["course_stream"] = "BUS"  # Default course stream

# Access the current city, country, and university from session state
current_city = st.session_state["source_city"]
country_of_study = st.session_state["country_of_study"]
university_name = st.session_state["university_name"]

st.title("Personalized Nudges Based on Course Type")

# Options for the select box
course_stream = ['BUS', 'STEM']

# Safely select the default index
default_index = course_stream.index(st.session_state["course_stream"]) if st.session_state["course_stream"] in course_stream else 0

# Display the select box
course_stream_selected = st.selectbox(
    "Select the stream you want to study:",
    course_stream,
    index=default_index
)

st.session_state["course_stream"] = course_stream_selected

submit = st.button("Submit")
data_analysis_course_type = course_type_analysis(data = filtered_data, course_type = course_stream_selected, source_city = current_city, country_of_study = country_of_study, university_name = university_name)
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
    if data_analysis_course_type:
        print("data_analysis_course_type ", data_analysis_course_type)
        random_result = random.choice(data_analysis_course_type)
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
