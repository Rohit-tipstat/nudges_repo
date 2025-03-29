import streamlit as st
import pandas as pd
from utils.data_analysis import course_name_analysis  # Import the new analysis function
from helper_function.helper import remove_outliers_iqr_specific_columns
from utils.llm_response import custom_nudges
import time
import random

filtered_data = pd.read_excel("/home/ubuntu/app/data/output.xlsx")

# Initialize session state variables
if "source_city" not in st.session_state:
    st.session_state["source_city"] = ""

if "country_of_study" not in st.session_state:
    st.session_state["country_of_study"] = ""

if "university_name" not in st.session_state:
    st.session_state["university_name"] = ""

if "course_name_selected" not in st.session_state:
    st.session_state["course_name_selected"] = ""

# Access session state variables safely
country_of_study = st.session_state["country_of_study"]
university_name = st.session_state["university_name"]
course_name_selected = st.session_state["course_name_selected"]
source_city = st.session_state['source_city']

# Streamlit UI
st.title("Personalized Analysis Based on Course Name")

# Options for Course Name selection
course_name_options = filtered_data['Course Name'].dropna().unique().tolist()

course_name_selected = st.selectbox(
    "Select the Course Name:", course_name_options
)

# Perform Analysis when button is clicked
data_analysis_course_name = course_name_analysis(
        data=filtered_data,
        course_name=course_name_selected,
        source_city=source_city,
        country_of_study=country_of_study,
        university_name=university_name
    )
submit = st.button("Analyze")


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
    if data_analysis_course_name:
        print("data_analysis_course_name ", data_analysis_course_name)
        random_result = random.choice(data_analysis_course_name)
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
