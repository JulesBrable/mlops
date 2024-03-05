"""Streamlit Homepage"""

import streamlit as st

from src.utils.etl import get_recommendations, show_recommendations
from src.utils.map import generate_map

st.set_page_config(
    page_title="Paris Events Recommender",
    page_icon="🎉",
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

query = st.sidebar.text_input("Enter your query:", "Sortie familiale en nature")

if st.button("Press this to get your recommendation"):
    if query:
        with st.spinner('🧠 Searching for recommendations using NLP...'):
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
else:
    st.write("Please enter a query to get recommendations.")
