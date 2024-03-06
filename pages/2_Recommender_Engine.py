"""Recommender Engine"""

import streamlit as st
from langdetect import detect

from src.utils.etl import preprocess_df, get_recommendations, show_recommendations
from src.utils.map import generate_map
from src.utils.translation import lead_text_translator, translate_query
from src.utils.utils import load_content, make_config, load_style, to_excel, download_results


make_config()
load_style()
content = load_content('assets/content/page2.json')

st.columns([1/100, 98/100, 1/100])[1].title(":tada: Paris Events Recommender")

query = st.sidebar.text_input(
    "**Enter your query:**",
    "Sortie familiale en nature",
    help="_Please enter an event idea on which to query the recommendation engine._"
    )

reco_button = st.sidebar.button("Press this to get your event recommendations", type="primary")

if 'recommendations' not in st.session_state or reco_button:
    if query and reco_button:
        with st.spinner(content["spinner_nlp"]):
            source_language = detect(query)
            query_french = translate_query(source_language, query)
            recommendations = get_recommendations(query_french)
        st.success('Recommendations Done!')

        if (recommendations is not None) and (not recommendations.empty):
            recommendations = preprocess_df(recommendations)
            if source_language != 'fr':
                with st.spinner(content["spinner_translator"]):
                    recommendations = lead_text_translator(
                        df=recommendations,
                        column_names=['Chapeau', 'Description'],
                        target=source_language
                        )
                st.success('Translation Done!')
            st.session_state.recommendations = recommendations
        else:
            st.markdown("No recommendations found for your query.")

if 'recommendations' in st.session_state and not st.session_state.recommendations.empty:
    show_recommendations(st.session_state.recommendations)
    generate_map(st.session_state.recommendations)
    df_xlsx = to_excel(st.session_state.recommendations)
    download_results(df_xlsx)
