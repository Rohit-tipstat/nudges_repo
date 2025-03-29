import streamlit as st
from utils.data_analysis import country_selected
import pandas as pd
from helper_function.helper import remove_outliers_iqr_specific_columns
from utils.llm_response import custom_nudges
import random
import time

data = pd.read_excel("/home/ubuntu/app/data/output.xlsx")

filtered_data = remove_outliers_iqr_specific_columns(data, ['Total COE'])
# Initialize session state for country_of_study
if "country_of_study" not in st.session_state or st.session_state["country_of_study"] not in ['AUSTRALIA', 'CANADA', 'UNITED STATES OF AMERICA', 'UNITED KINGDOM']:
    st.session_state["country_of_study"] = "AUSTRALIA"


if "source_city" not in st.session_state:
    st.session_state["source_city"] = "Unknown"

current_city = st.session_state["source_city"]

print("Current city", current_city)
st.title("Personalized Nudges Based on Country of Education")

# Options for the select box
country_options = ['AUSTRALIA', 'CANADA', 'UNITED STATES OF AMERICA', 'UNITED KINGDOM']

# Safely select the default index
default_index = country_options.index(st.session_state["country_of_study"])

# Display the select box
country_of_study_ = st.selectbox(
    "Select the country you want to study in:",
    country_options,
    index=default_index
)
st.session_state["country_of_study"] = country_of_study_

result_analysis = country_selected(data=filtered_data, country_of_study=country_of_study_, source_city = current_city)


# Button to trigger notification generation
if st.button("Submit", key="submit_button"):
    start = time.time()

    nudges_list = []

    # for result in result_analysis:
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

        # Select a random result from the analysis if available
    if result_analysis:
        random_result = random.choice(result_analysis)
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


