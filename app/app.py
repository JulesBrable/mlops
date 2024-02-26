import streamlit as st
import pandas as pd

from model.recommendation import Recommender

st.title("Recommendation System")

query = st.sidebar.text_input("Enter your query:", "Sortie familiale en nature")


@st.cache_data
def load_data():
    df = pd.read_csv("https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv", sep=";")
    return df


@st.cache_resource()
def load_recommender():
    df = load_data()
    recommender = Recommender(df)
    return recommender


def show_recommendations(query):
    if query:
        recommender = load_recommender()
        recommendations = recommender.get_recommendations(query)
        if recommendations is not None and not recommendations.empty:
            st.write("Recommendations:")
            st.dataframe(recommendations, hide_index=True)
        else:
            st.write("No recommendations found for your query.")


if st.button("Press this to get your recommendation"):
    if query:
        show_recommendations(query)
else:
    st.write("Please enter a query to get recommendations.")
