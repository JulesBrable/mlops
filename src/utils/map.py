"""Utils for the Folium Map that is being displayed in the Streamlit App"""

import folium
from streamlit_folium import folium_static


def add_markers_to_map(m, recommendations):
    """
    Adds interactive markers for event recommendations to a map.
    This function iterates through each event recommendation in the provided DataFrame
    and adds a marker to the map (`m`) for each event. The markers are interactive,
    displaying a popup with detailed information about the event when clicked.
    The popup includes the event's title, summary, venue name, address, and start date.

    Parameters:
        m (folium.Map): The map object to which the markers will be added.
        recommendations (pd.DataFrame): A DataFrame containing event recommendations.

    Returns:
        None: This function modifies the map object in place and does not return any value.
    """
    for _, row in recommendations.iterrows():
        tooltip = f"<strong>{row['Titre']}</strong><br>"
        html = popup_html(
            titre=row['Titre'],
            chapeau=row['Chapeau'],
            lieu=row['Nom du lieu'],
            adresse=row['Adresse du lieu'],
            date=row['Date de début']
        )
        popup = folium.Popup(folium.Html(html, script=True), parse_html=True)
        icon = 'eye-open'
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color='darkred', icon=icon)
        ).add_to(m)


def generate_map(recommendations):
    """
    Generates an interactive map using Folium, centered on the mean location of the given
    recommendations. This map is then populated with markers for each recommendation,
    including customized tooltips and popups with detailed information.

    Parameters:
        recommendations (pandas.DataFrame): A DataFrame containing the recommendations data.

    Returns:
        None: The function creates and displays an interactive map using Folium.
    """
    location = recommendations[['Latitude', 'Longitude']]
    m = folium.Map(location=location.mean().values.tolist())
    add_markers_to_map(m, recommendations)

    sw = location.min().values.tolist()
    ne = location.max().values.tolist()
    m.fit_bounds([sw, ne])
    folium_static(m)


def popup_html(titre, chapeau, lieu, adresse, date):
    """
    Creates a customized popup for the folium map, using HTML and CSS.
    Allows to give more specific information about a given point of the map.
    """

    html = f"""<!DOCTYPE html>
    <html>
        <head>
            <style>
                p {{
                  background-color: #00a0a0;
                  color: white;
                  padding: 10px 10px 10px 10px;
                  border: 2px solid #101357;
                  border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <p>
                <strong>{titre}</strong>&nbsp;{chapeau}
                <br>
                <strong>{lieu}:</strong>&nbsp;{adresse}&nbsp;seconds
                <br>
                <strong>Date:</strong>&nbsp;{date}
            </p>
        </body>
    </html>"""

    return html
