"""Recommender Engine"""
import streamlit as st
from langdetect import detect

from src.utils.etl import load_data, preprocess_df, get_recommendations, filter_df
from src.utils.map import generate_map
from src.utils.translation import lead_text_translator, translate_query
from src.utils.utils import load_content, make_config, load_style, to_excel
import src.utils.page1_ui as p1

make_config()
load_style()
content = load_content('assets/content/page1.json')

st.columns([1/100, 98/100, 1/100])[1].title(":tada: Paris Events Recommender")

query = st.sidebar.text_input(
    "**Enter your query:**",
    "Sortie familiale en nature",
    help=content["help_input"]
    )

df = load_data()
df = preprocess_df(df, content["col_list"])

tabs = st.tabs(["Filtering criteria & Statistics", "Recommender Results"])

with tabs[0]:
    st.markdown("### Filters")
    st.markdown(
        """In this section, you can filter events according to various criteria. You are
        then invited to consult the statistics calculated below and/or query our recommendation
        engine (recommendations will be made on the basis of filtered events)."""
        )

    cols = st.columns(2, gap="medium")
    with cols[0]:
        price = p1.create_expander_multiselect("Filter by pricing type", df, "Type de prix")
        audience = p1.create_expander_multiselect("Filter by audience type", df, "audience")
        city = p1.create_expander_multiselect("Filter by city", df, "Ville")
        if "Paris" in city:
            arr = p1.create_expander_multiselect("Filter by arrondissement", df, "Arrondissement")
        else:
            arr = None
        reservation = p1.create_expander_multiselect("Filter by booking type", df, "Type d'accès")

        st.markdown("##### Specific choices for disabled access:")
        subcols = st.columns(3)
        with subcols[0]:
            amv = st.toggle("With blind access", value=False)
        with subcols[1]:
            ame = st.toggle("With hearing-impaired access", value=False)
        with subcols[2]:
            apmr = st.toggle("With access for the mobility impaired", value=False)
    filters = [f if f else None for f in [city, arr, price, reservation, audience, amv, ame, apmr]]
    df = filter_df(df, filters)

    with cols[1]:
        subsubcols = st.columns(2)
        with st.columns([1/5, 3/5, 1/5])[1]:
            st.metric("Number of events", df.shape[0])

        st.markdown("""
        ##### Let's look at the most present words to inspire you for your query!
        Select a wordcloud type:
        """)
        grams = st.radio(
            "e", ["Uni-grams", "Bi-grams"], horizontal=True, label_visibility="collapsed"
            )
        wordcloud = p1.plot_wordcloud(df, grams)

    st.markdown("### Charts")
    p1.plot_category_distributions(df, ["Type de prix", "audience", "Type d'accès"])
    p1.plot_category_distributions(df, ["Accès mal voyant", "Accès mal entendant", "Accès PMR"])

reco_button = st.sidebar.button("Press this to get your event recommendations", type="primary")

with tabs[1]:
    if not reco_button:
        st.markdown("Please query our recommender engine from the sidebar panel! 😊")
    if 'recommendations' not in st.session_state or reco_button:
        if query and reco_button:
            with st.spinner(content["spinner_nlp"]):
                source_language = detect(query)
                query_french = translate_query(source_language, query)
                recommendations = get_recommendations(df, query_french)
            st.success(f"Recommendations done: {recommendations.shape[0]} events found!")

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
    else:
        pass
    if 'recommendations' in st.session_state and not st.session_state.recommendations.empty:
        p1.show_recommendations(st.session_state.recommendations)
        generate_map(st.session_state.recommendations)
        df_xlsx = to_excel(st.session_state.recommendations)
        p1.download_results(df_xlsx)
