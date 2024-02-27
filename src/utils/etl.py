"""ETL pipelines that are being used in the Streamlit App"""

import streamlit as st
import pandas as pd
from src.models.recommendation import Recommender


@st.cache_data
def load_data():
    """Loads event data from a specified CSV file hosted online."""
    df = pd.read_csv("https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv", sep=";")
    return df


@st.cache_resource()
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
    st.write("Recommendations:")
    for _, row in recommendations.iterrows():
        with st.expander(rf":pencil2:  **{row['Titre']}** - {row['Chapeau']}"):
            st.write(f"**Description:** {row['Description']}")
            st.write(f"**Date:** {row['Date de début']} - {row['Date de fin']}")
            st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
