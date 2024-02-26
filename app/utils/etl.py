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
