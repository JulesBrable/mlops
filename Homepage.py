import streamlit as st
from src.utils.utils import load_content, make_config

make_config()

content = load_content('assets/content/page0.json')

st.title(content["welcome"])
st.markdown(content["intro"])

st.header(content["how_it_works_header"])
st.markdown(content["how_it_works_content"])

st.header(content["our_data_header"])
st.markdown(content["our_data_content"])

st.header(content["getting_started_header"])
st.markdown(content["getting_started_content"])

st.header(content["maximizing_experience_header"])
st.markdown(content["maximizing_experience_content"])

st.markdown(content["ready_to_explore"])
