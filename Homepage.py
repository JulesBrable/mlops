"""Streamlit Homepage"""

import streamlit as st


st.set_page_config(
    page_title="Paris Events Recommender",
    page_icon=":tada:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/JulesBrable/mlops/issues/new",
        'About': """
        If you want to read more about the project, you would be interested in going to the
        corresponding [GitHub](https://github.com/JulesBrable/mlops) repository.

        Contributions:
        - [Jules Brablé](linkedin.com/in/jbrable)
        - [Martin Boutier]()
        - [Louis Latournerie]()

        """
    }
)

st.markdown("Some presentation elements about the app & its purpose")
