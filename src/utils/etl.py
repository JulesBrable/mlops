"""ETL pipelines that are being used in the Streamlit App"""
import streamlit as st
import pandas as pd
from dateutil import parser
from wordcloud import WordCloud
from stop_words import get_stop_words
from src.models.recommendation import Recommender
from nltk.util import bigrams
import nltk
from collections import Counter

@st.cache_data(show_spinner=False)
def load_data():
    """Loads event data from a specified CSV file hosted online."""
    # df = pd.read_csv("https://minio.lab.sspcloud.fr/jbrablx/mlops/data/raw/data.csv", sep=";")
    df = pd.read_csv("data.csv", sep=";")
    return df


@st.cache_resource(show_spinner=False)
def load_recommender():
    """Initializes and returns a Recommender system instance."""
    df = load_data()
    recommender = Recommender(df)
    return recommender

@st.cache_resource(show_spinner=False)
def plot_wordclout():
    df = load_data()
    text = " ".join(str(review) for review in df['Mots clés'] if review and not pd.isnull(review))
    stopwords = set(get_stop_words('french'))
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400, mode="RGBA").generate(text)
    return wordcloud

@st.cache_resource(show_spinner=False)
def plot_wordclout_from_bigrams():
    
    df = load_data()
    data = df['Mots clés'].astype(str).values.tolist()
    filtered_data = [item.split(',') for item in data if item != 'nan']
    
    bigram_list = [bigram for sublist in filtered_data for bigram in bigrams(sublist)]
    bigram_strings = ['/'.join(bigram) for bigram in bigram_list]
    
    bigram_frequency = Counter(bigram_strings)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(bigram_frequency)
    return wordcloud
    
def get_recommendations(query):
    """Fetches recommendations based on a user query."""
    recommender = load_recommender()
    return recommender.get_recommendations(query)


def get_digest_date(date_col):
    return parser.parse(date_col).strftime('%B %d, %Y, %H:%M')


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
            From {get_digest_date(row['Date de début'])}
            to {get_digest_date(row['Date de fin'])}
            """)
            st.write(f"**Plus d'informations en cliquant [ici]({row['URL']}).**")
            
            

