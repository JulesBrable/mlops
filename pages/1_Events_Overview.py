import streamlit as st
from src.utils.etl import plot_wordclout, plot_wordclout_from_bigrams
import matplotlib.pyplot as plt
from src.utils.utils import make_config


make_config()

st.title("Dive into the Buzz 🐝")
st.markdown("### Some descriptive statistics here about previous & future events")

fig, ax = plt.subplots()
wordcloud = plot_wordclout()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)


st.markdown("### Let's look at words associations (bigrams) to inspire you more for your query, and even give you some ideas !")
fig, ax = plt.subplots()
wordcloud = plot_wordclout_from_bigrams()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)