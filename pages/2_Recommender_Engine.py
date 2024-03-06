"""Recommender Engine"""

import streamlit as st
from langdetect import detect

from src.utils.etl import load_data, preprocess_df, get_recommendations, show_recommendations
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

df = load_data()

df = preprocess_df(df, content["col_list"])

tabs = st.tabs(["Filters", "Results"])
with tabs[0]:
    city = st.multiselect("**Select a city:**", list(df["Ville"].unique()), default=list(df["Ville"].unique()))
    arr = st.multiselect("**Select an arrondissement:**", list(df["Arrondissement"].unique()), default=list(df["Arrondissement"].unique()))
    price = st.multiselect("**Type de prix**", list(df["Type de prix"].unique()), default=list(df["Type de prix"].unique()))
    amv = st.multiselect("**Select a amv:**", list(df["Accès mal voyant"].unique()), default=list(df["Accès mal voyant"].unique()))
    ame = st.multiselect("**Select a ame:**", list(df["Accès mal entendant"].unique()), default=list(df["Accès mal entendant"].unique()))
    apmr = st.multiselect("**Select a apmr:**", list(df["Accès PMR"].unique()), default=list(df["Accès PMR"].unique()))
    reservation = st.multiselect("**Select a reservation:**", list(df["Type d'accès"].unique()), default=list(df["Type d'accès"].unique()))
    audience = st.multiselect("**Select an audience:**", list(df["audience"].unique()), default=list(df["audience"].unique()))

df = df[df["Ville"].isin(city)]

reco_button = st.sidebar.button("Press this to get your event recommendations", type="primary")

with tabs[1]:
    if 'recommendations' not in st.session_state or reco_button:
        if query and reco_button:
            with st.spinner(content["spinner_nlp"]):
                source_language = detect(query)
                query_french = translate_query(source_language, query)
                recommendations = get_recommendations(df, query_french)
            st.success('Recommendations Done!')

            if (recommendations is not None) and (not recommendations.empty):
                recommendations = preprocess_df(recommendations, content["col_list"])
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
