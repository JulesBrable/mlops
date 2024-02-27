import streamlit as st
import pandas as pd
from model.recommendation import Recommender

@st.cache_data
def load_data():
    df = pd.read_csv("https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv", sep=";")
    return df


@st.cache_resource()
def load_recommender():
    df = load_data()
    recommender = Recommender(df)
    return recommender

def get_recommendations(query):
    recommender = load_recommender()
    return recommender.get_recommendations(query)

def show_recommendations(recommendations):
        st.write("Recommendations:")
        for index, row in recommendations.iterrows():
            with st.expander(rf":pencil2:  **{row['Titre']}** - {row['Chapeau']}"):
                st.write(f"**Description:** {row['Description']}")
                st.write(f"**Date:** {row['Date de début']} - {row['Date de fin']}")
                st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
