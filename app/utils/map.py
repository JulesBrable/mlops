

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