"""ETL pipelines that are being used in the Streamlit App"""
import pandas as pd
import numpy as np
import streamlit as st
from dateutil import parser
import re

from src.models.recommendation import Recommender


@st.cache_data(show_spinner=False)
def load_data(url: str = "https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv"):
    """Loads event data from a specified CSV file hosted online."""
    df = pd.read_csv(url, sep=";")
    return df


@st.cache_resource(show_spinner=False)
def load_recommender(df: pd.DataFrame):
    """Initializes and returns a Recommender system instance."""
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


def clean_audience(row):
    row = re.sub(' +', ' ', row)

    l = ["adultes", "enfants", "adolescents"]

    audience_conditions = {
        "Tout public": lambda r: "Tout public" in r or all(kw in r for kw in l),
        "Public enfants adolescents": lambda r: all(kw in r for kw in [l[1], l[2]]) and l[0] not in r,
        "Public enfants adultes": lambda r: all(kw in r for kw in [l[0], l[1]]) and l[2] not in r,
        "Public adolescents adultes": lambda r: all(kw in r for kw in [l[0], l[2]]) and l[1] not in r,
        "Public enfants": lambda r: l[1] in r and all(kw not in r for kw in [l[0], l[2]]),
        "Public adolescents": lambda r: l[2] in r and all(kw not in r for kw in [l[0], l[1]]),
        "Public adultes": lambda r: l[0] in r and all(kw not in r for kw in [l[1], l[2]]),
    }

    for response, condition in audience_conditions.items():
        if condition(row):
            return response
    return row


def preprocess_df(
    df,
    col_list,
    col_geo='Coordonnées géographiques',
    date_cols=["Date de début", "Date de fin"],
    col_ville="Ville",
    col_cp="Code postal"
):
    df = df[col_list]
    df = get_coordinates(df, col_geo)
    df["Département"] = df[col_cp].str[:2]
    df[col_ville] = np.where(df["Département"] == "75", "Paris", df[col_ville])
    df["Arrondissement"] = get_arrondissement(df, col_ville, col_cp)
    df["audience"] = df["audience"].apply(lambda x: clean_audience(x))
    
    for col in list(date_cols):
        df[col] = handle_na(df, col, "")

    for col in list(col_list + ["Arrondissement", "Département"]):
        df[col] = np.where(df[col].astype(str) == "nan", "Not specified", df[col])    
    return df


def filter_df(
    df: pd.DataFrame,
    filters
):
    df = df[df["Ville"].isin(filters[0])]
    if "Paris" in filters[0]:
        df = df[df["Arrondissement"].isin(filters[1])]
    df = df[df["Type de prix"].isin(filters[2])]
    df = df[df["Type d'accès"].isin(filters[3])]
    df = df[df["audience"].isin(filters[4])]
    df = df[df["Accès mal voyant"] == "1.0"] if filters[5] else df
    df = df[df["Accès mal entendant"] == "1.0"] if filters[6] else df
    df = df[df["Accès PMR"] == "1.0"] if filters[7] else df
    return df


def get_recommendations(df, query):
    """Fetches recommendations based on a user query."""
    recommender = load_recommender(df)
    return recommender.get_recommendations(query)


def get_digest_date(date_col):
    try:
        date_col = parser.parse(date_col).strftime('%B %d, %Y, %H:%M')
    except parser.ParserError:
        date_col = ""
    return date_col
