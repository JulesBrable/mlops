import folium
from streamlit_folium import folium_static

def add_markers_to_map(m, recommendations):
    for i, row in recommendations.iterrows():
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
    Allows to give more sepcific information about a given point of the map.
    """
    
    html = """<!DOCTYPE html>
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
    </html>""".format(**locals())
    
    return html