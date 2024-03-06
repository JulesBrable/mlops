"""ETL pipelines that are being used in the Streamlit App"""

import pandas as pd
import numpy as np
import streamlit as st
from dateutil import parser
import re

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


def handle_na(df, col, to_replace):
    return np.where(pd.isna(df[col]), to_replace, df[col])


def get_coordinates(df, col):
    df[['Latitude', 'Longitude']] = (
        df[col]
        .str
        .split(',', expand=True)
        .astype(float)
    )
    for sub_col in ["Latitude", "Longitude"]:
        df[sub_col] = handle_na(df, sub_col, None)
    return df


def get_arrondissement(df, col_ville, col_cp):
    df["cp_tempo"] = df[col_cp].apply(
        lambda x: "" if pd.isna(x) else re.sub(r'\s+|[^0-9]', '', str(x))[3:5]
        )
    df["cp_tempo"] = df["cp_tempo"].apply(lambda x: '0' + x if len(x) < 2 and x != "" else x)
    df["cp_tempo"] = np.where(df[col_ville] == "Paris", df["cp_tempo"], np.nan)
    df.loc[df["cp_tempo"].eq("00"), "cp_tempo"] = np.nan
    return df["cp_tempo"].values


def preprocess_df(
    df,
    col_geo='Coordonnées géographiques',
    date_cols=["Date de début", "Date de fin"],
    col_ville="Ville",
    col_cp="Code postal"
):
    df = get_coordinates(df, col_geo)
    df["Département"] = df[col_cp].str[:2]
    df[col_ville] = np.where(df["Département"] == "75", "Paris", df[col_ville])
    df["Arrondissement"] = get_arrondissement(df, col_ville, col_cp)

    for col in list(date_cols):
        df[col] = handle_na(df, col, "")
    return df


def get_recommendations(query):
    """Fetches recommendations based on a user query."""
    recommender = load_recommender()
    return recommender.get_recommendations(query)


def get_digest_date(date_col):
    try:
        date_col = parser.parse(date_col).strftime('%B %d, %Y, %H:%M')
    except parser.ParserError:
        date_col = ""
    return date_col


def show_recommendations(recommendations):
    """Displays recommendations in an interactive format using Streamlit."""
    st.markdown(
        "##### Recommendations:",
        help="Click on the expander for more info about the event"
        )
    for _, row in recommendations.iterrows():
        with st.expander(rf":pencil2:  **{row['Titre']}** - {row['Chapeau']}"):
            st.markdown(f"**Description:** {row['Description']}", unsafe_allow_html=True)
            if (row['Date de début'] != "") and (row['Date de fin'] != ""):
                st.write(f"""
                **Date:**
                From {get_digest_date(row['Date de début'])}
                to {get_digest_date(row['Date de fin'])}
                """)
            st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
