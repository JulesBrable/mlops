"""ETL pipelines that are being used in the Streamlit App"""

import streamlit as st
import pandas as pd
from dateutil import parser

from src.models.recommendation import Recommender


@st.cache_data(show_spinner=False)
def load_data():
    """Loads event data from a specified CSV file hosted online."""
    df = pd.read_csv("https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv", sep=";")
    return df


@st.cache_resource(show_spinner=False)
def load_recommender():
    """Initializes and returns a Recommender system instance."""
    df = load_data()
    recommender = Recommender(df)
    return recommender


def get_recommendations(query):
    """Fetches recommendations based on a user query."""
    recommender = load_recommender()
    return recommender.get_recommendations(query)


def show_recommendations(recommendations):
    """Displays recommendations in an interactive format using Streamlit."""
    st.markdown(
        "Recommendations:",
        help="Click on the expander for more info about the event"
        )
    for _, row in recommendations.iterrows():
        with st.expander(rf":pencil2:  **{row['Titre']}** - {row['Chapeau']}"):
            st.markdown(f"**Description:** {row['Description']}", unsafe_allow_html=True)
            st.write(f"""
            **Date:**
            From {parser.parse(row['Date de début']).strftime('%B %d, %Y, %H:%M')}
            to {parser.parse(row['Date de fin']).strftime('%B %d, %Y, %H:%M')}
            """)
            st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
