import json
import streamlit as st
from io import BytesIO
import pandas as pd


def load_content(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def make_config(file_path: str = 'assets/config.json'):
    config = load_content(file_path)
    st.set_page_config(**config)


def load_style(style_path: str = "assets/styles.css"):
    with open(style_path) as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)


@st.cache_data
def to_excel(res):
    """
    Converts recommendation results and model parameters into an Excel file.

    Parameters:
    - res (DataFrame): A pandas DataFrame containing the recommendation results.

    Returns:
    - BytesIO: A buffer containing the Excel file.

    Decorators:
    - @st.cache_data: Caches the output of this function to avoid regenerating the Excel
      file from the same DataFrames multiple times.
    """
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        res.to_excel(writer, sheet_name='Results', index=False)
    return buffer
