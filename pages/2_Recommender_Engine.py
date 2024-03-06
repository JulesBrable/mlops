"""Recommender Engine"""

import streamlit as st

from src.utils.etl import get_recommendations, show_recommendations
from src.utils.map import generate_map
from src.utils.translation import query_to_french, lead_text_translator
from langdetect import detect

st.columns([1/100, 98/100, 1/100])[1].title(":tada: Paris Events Recommender")

with open("./styles.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

query = st.sidebar.text_input(
    "**Enter your query:**",
    "Sortie familiale en nature",
    help="_Please enter an event idea on which to query the recommendation engine._")

if st.button("Press this to get your event recommendations", type="primary"):
    if query:
        with st.spinner(':brain: _Searching for recommendations using NLP..._'):
            source_language = detect(query)
            if source_language == 'fr':
                query_french = query + ''
            else:
                query_french = query_to_french(query)

            recommendations = get_recommendations(query_french)

        if source_language != 'fr':
            with st.spinner(':brain: _Translation of the results..._'):
                recommendations = lead_text_translator(
                    df=recommendations,
                    column_names=['Chapeau', 'Description'],
                    target=source_language)
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
