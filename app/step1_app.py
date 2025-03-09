import streamlit as st

st.set_page_config(page_title="Animated Nudges")

st.title("Personalized Nudges")

# Ensure source_city has a valid default
if "source_city" not in st.session_state:
    st.session_state["source_city"] = "BENGALURU"

city_options = ['AHMEDABAD', 'BENGALURU', 'CHENNAI', 'DELHI', 'HYDERABAD', 'MUMBAI', 'PUNE']

# Ensure session state value is valid in city options
default_index = city_options.index(st.session_state['source_city']) if st.session_state['source_city'] in city_options else 0

name = st.text_input("Enter your Name:")
source_city = st.selectbox("Select the current city:", city_options, index=default_index)
submit = st.button("Submit")

if submit:
    st.session_state['source_city'] = source_city
    st.write(f"You have selected {source_city} as your current city.")
