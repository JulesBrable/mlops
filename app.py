"""Streamlit Homepage"""

import streamlit as st

from src.utils.etl import get_recommendations, show_recommendations
from src.utils.map import generate_map

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

st.columns([1/100, 98/100, 1/100])[1].title(":tada: Paris Events Recommender")

st.markdown("""
  <style>
  div.stButton {text-align:center}
  </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
    }
    </style>""", unsafe_allow_html=True)

query = st.sidebar.text_input(
    "**Enter your query:**",
    "Sortie familiale en nature",
    help="_Please enter an event idea on which to query the recommendation engine._")

if st.button("Press this to get your event recommendations", type="primary"):
    if query:
        with st.spinner(':brain: Searching for recommendations using NLP...'):
            recommendations = get_recommendations(query)
        st.success('Done!')

        if recommendations is not None and not recommendations.empty:
            recommendations[['Latitude', 'Longitude']] = (
                recommendations['Coordonnées géographiques']
                .str
                .split(',', expand=True)
                .astype(float)
            )
            show_recommendations(recommendations)
            generate_map(recommendations)
        else:
            st.write("No recommendations found for your query.")
