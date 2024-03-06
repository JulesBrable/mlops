import streamlit as st

# Set up page configuration
st.set_page_config(
    page_title="Paris Events Recommender",
    page_icon=":tada:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/JulesBrable/mlops/issues/new",
        'About': """
        If you want to read more about the project, you would be interested in going to the
        corresponding [GitHub](https://github.com/JulesBrable/mlops) repository.

        Contributions:
        - [Jules Brablé](https://linkedin.com/in/jbrable)
        - Martin Boutier
        - Louis Latournerie

        """
    }
)

# Introduction to the app
st.title("Welcome to the Paris Events Recommender! :fr:")
st.markdown("""
This Streamlit app is your go-to source for finding the best events in Paris tailored to your interests. 
Whether you're looking for activities, sports, relaxation spots, top-notch restaurants, or enriching museum visits, 
we've got you covered. :sparkles:
""")

# About the model
st.header("How It Works :mag_right:")
st.markdown("""
Our app utilizes the powerful Language Model BERT from Hugging Face, specifically designed to understand the nuances of your preferences.
By analyzing your interests with this state-of-the-art model, we recommend events that match your tastes perfectly. 

Learn more about BERT and its capabilities on [Hugging Face](https://huggingface.co/sentence-transformers). :rocket:
""")

# Data source
st.header("Our Data :floppy_disk:")
st.markdown("""
The events recommended by our app are sourced from the comprehensive "Que faire à Paris?" dataset provided by OpenDataSoft.
This dataset includes a wide variety of events happening around Paris, ensuring you're always in the loop with the latest and greatest activities.

Discover more about the data [here](https://data.opendatasoft.com/explore/dataset/que-faire-a-paris-%40parisdata/export/?disjunctive.tags&disjunctive.address_name&disjunctive.address_zipcode&disjunctive.address_city&disjunctive.pmr&disjunctive.blind&disjunctive.deaf&disjunctive.price_type&disjunctive.access_type&disjunctive.programs). :link:
""")

# App usage instructions
st.header("Getting Started :runner:")
st.markdown("""
To start receiving personalized event recommendations, simply input your interests in the sidebar and let our model do the rest.
Whether you're a long-time Paris resident or just visiting, our app will help you discover the city in new and exciting ways. :city_sunrise:
""")

# Adding more content
st.header("Maximizing Your Experience :bulb:")
st.markdown("""
While our app is designed to bring you the best of Paris, there are times when you might not find exactly what you're looking for on the first try. This could be due to a few reasons:

- **Limited Data**: There might be fewer events available than usual, limiting the diversity of recommendations.
- **Vague Queries**: A broad or unclear input can make it challenging for our model to find the perfect match.

**Tips for Better Results**:
- **Be Specific**: Use clear and detailed queries. For example, instead of just "art", try "modern art exhibitions".
- **Retry**: If the first set of recommendations doesn't satisfy you, refine your interests and try again.

Remember, the more information you provide, the better our model can tailor the recommendations to your taste. :dart:
""")

st.markdown("### Ready to explore Paris? Let's get started! :rocket:")
