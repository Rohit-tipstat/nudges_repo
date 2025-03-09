import streamlit as st
from utils.data_analysis import university_selected
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

# University options based on the selected country
university_options = {
    "UNITED STATES OF AMERICA": ["HARVARD UNIVERSITY", "ARIZONA STATE UNIVERSITY", "COLUMBIA UNIVERSITY"],
    "CANADA": ["CANADA COLLEGE", "UNIVERSITY CANADA WEST UCW", "THE UNIVERSITY OF BRITISH COLUMBIA"],
    "UNITED KINGDOM": ["BIRMINGHAM CITY UNIVERSITY", "QUEEN MARY UNIVERSITY OF LONDON", "IMPERIAL COLLEGE LONDON"],
    "AUSTRALIA": ["MELBOURNE INSTITUTE OF TECHNOLOGY", "THE UNIVERSITY OF ADELAIDE", "VICTORIA UNIVERSITY"]
}

# Access the current city and country from session state
current_city = st.session_state["source_city"]
country_of_study = st.session_state["country_of_study"]

st.title("Personalized Nudges Based on University Selection")

# Display dynamic university options based on the selected country
if country_of_study:
    universities = university_options.get(country_of_study, [])
    
    if universities:
        # Safely determine the default index
        default_index = universities.index(st.session_state["university_name"]) if st.session_state["university_name"] in universities else 0

        university_name_ = st.selectbox(
            f"Select the university you want to study in ({country_of_study}):",
            universities, index=default_index
        )
        
        # Store the selected university in session state
        st.session_state["university_name"] = university_name_


submit = st.button("Submit")
data_analysis_for_university = university_selected(data = filtered_data, university_name = university_name_, source_city = current_city)

if submit:
    nudges_list = []
    start = time.time()

    # for result in data_analysis_for_university:
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
    
    if data_analysis_for_university:
        print("data_analysis_for_university ", data_analysis_for_university)
        random_result = random.choice(data_analysis_for_university)
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
