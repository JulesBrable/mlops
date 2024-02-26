import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static

from utils.etl import load_data, load_recommender
from utils.map import popup_html

st.set_page_config(
    page_title="Paris Events Recommender",
    page_icon="🎉",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/JulesBrable/mlops/issues/new",
        'About': """ 
        If you want to read more about the project, you would be interested in going to the corresponding
        [GitHub](https://github.com/JulesBrable/mlops) repository.
        
        Contributions:
        - [Jules Brablé](linkedin.com/in/jbrable)
        - [Martin Boutier]()
        - [Louis Latournerie]()
        
        """
    }
)

st.title("Recommendation System")

query = st.sidebar.text_input("Enter your query:", "Sortie familiale en nature")

def show_recommendations(query):
    if query:
        recommender = load_recommender()
        recommendations = recommender.get_recommendations(query)
        if recommendations is not None and not recommendations.empty:
            st.write("Recommendations:")
            for index, row in recommendations.iterrows():
                
                with st.expander(rf":pencil2:  **{row['Titre']}** - {row['Chapeau']}"):

                    st.write(f"**Description:** {row['Description']}")
                    st.write(f"**Date:** {row['Date de début']} - {row['Date de fin']}")
                    st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
            recommendations[['Latitude', 'Longitude']] = recommendations['Coordonnées géographiques'].str.split(',', expand=True).astype(float)
            
            location = recommendations[['Latitude', 'Longitude']]
            m = folium.Map(location=location.mean().values.tolist())

            for i, row in recommendations.iterrows():
                tooltip = f"<strong>{row['Titre']}</strong><br>"
                html = popup_html(
                    titre=row['Titre'],
                    chapeau=row['Chapeau'],
                    lieu=row['Nom du lieu'],
                    adresse=row['Adresse du lieu'],
                    date=row['Date de début']
                )
                popup = folium.Popup(folium.Html(html, script=True), parse_html=True)
                icon = 'eye-open'
                folium.Marker(
                    location = [row['Latitude'], row['Longitude']],
                    popup = popup,
                    tooltip = tooltip,
                    icon = folium.Icon(color='darkred', icon=icon)
                ).add_to(m)
                
            sw = location.min().values.tolist()
            ne = location.max().values.tolist()
            m.fit_bounds([sw, ne])
            
            folium_static(m)
            
        else:
            st.write("No recommendations found for your query.")


if st.button("Press this to get your recommendation"):
    if query:
        show_recommendations(query)
else:
    st.write("Please enter a query to get recommendations.")
