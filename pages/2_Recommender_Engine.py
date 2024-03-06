"""Recommender Engine"""

import streamlit as st
from langdetect import detect

from src.utils.etl import preprocess_df, get_recommendations, show_recommendations
from src.utils.map import generate_map
from src.utils.translation import query_to_french, lead_text_translator
from src.utils.utils import load_content, make_config


make_config()

st.columns([1/100, 98/100, 1/100])[1].title(":tada: Paris Events Recommender")

with open("assets/styles.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

content = load_content('assets/content/page2.json')

query = st.sidebar.text_input(
    "**Enter your query:**",
    "Sortie familiale en nature",
    help="_Please enter an event idea on which to query the recommendation engine._")

if st.sidebar.button("Press this to get your event recommendations", type="primary"):
    if query:
        with st.spinner(content["spinner_nlp"]):
            source_language = detect(query)
            if source_language == 'fr':
                query_french = query + ''
            else:
                query_french = query_to_french(query)

            recommendations = get_recommendations(query_french)
        st.success('Recommendations Done!')

        if recommendations is not None and not recommendations.empty:
            recommendations = preprocess_df(
                recommendations, 'Coordonnées géographiques', ["Date de début", "Date de fin"]
                )
            if source_language != 'fr':
                with st.spinner(content["spinner_translator"]):
                    recommendations = lead_text_translator(
                        df=recommendations,
                        column_names=['Chapeau', 'Description'],
                        target=source_language)
                st.success('Translation Done!')

            show_recommendations(recommendations)
            generate_map(recommendations)
        else:
            st.write("No recommendations found for your query.")
