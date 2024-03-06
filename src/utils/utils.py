import json
import streamlit as st


def load_content(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def make_config(file_path: str = 'assets/config.json'):
    config = load_content(file_path)
    st.set_page_config(**config)


def load_style(style_path: str = "assets/styles.css"):
    with open(style_path) as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
