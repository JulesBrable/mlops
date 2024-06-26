"""Implement our NLP-based Recommendation Engine"""
from typing import List
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class Recommender:
    """
    Implements a recommender system using Sentence-BERT for semantic text embedding and cosine
    similarity for generating recommendations based on textual similarity.

    Attributes:
        df (pd.DataFrame): DataFrame containing data for recommendations.
        model (SentenceTransformer): Pre-loaded Sentence-BERT model for text embedding.

    Methods:
        __init__(self, df: pd.DataFrame):
            Initializes the recommender with data and a Sentence-BERT model.

        compute_embeddings(self, texts: List[str]) -> np.ndarray:
            Computes and returns embeddings for a list of text strings.

        get_recommendations(self, query: str, similarity_threshold: float = 0.51) -> pd.DataFrame:
            Returns recommendations for a given query, based on a similarity threshold.
    """
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the Recommender with a pandas DataFrame and loads the Sentence-BERT model.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the recommendation data.
        """
        self.df = df
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Computes embeddings for a list of texts using the Sentence-BERT model.

        Parameters:
            texts (List[str]): Texts to encode into embeddings.

        Returns:
            np.ndarray: The computed embeddings.
        """
        return self.model.encode(texts)

    def get_recommendations(self, query: str, similarity_threshold: float = 0.51) -> pd.DataFrame:
        """
        Retrieves DataFrame rows as recommendations based on semantic similarity to the query.

        Parameters:
            query (str): The query text for finding similar items.
            similarity_threshold (float, optional): Threshold for cosine similarity (default: 0.51).

        Returns:
            pd.DataFrame: Recommended items.
        """
        texts = self.df['Chapeau'].str.lower().tolist() + [query.lower()]
        embeddings = self.compute_embeddings(texts)

        query_embedding = embeddings[-1].reshape(1, -1)
        cosine_sim = cosine_similarity(query_embedding, embeddings[:-1])[0]

        top_indices = np.argsort(cosine_sim)[::-1][:4]

        return self.df.iloc[top_indices]
