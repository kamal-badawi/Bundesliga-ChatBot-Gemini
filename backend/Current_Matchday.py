# Gibt den Namen und die Nummer des aktuellen Bundesligaspieltags zurück
def fetch_current_matchday() -> dict:
    import requests
    import pandas as pd


    # API-Endpunkt für den aktuellen Spieltag
    url_current_matchday = "https://api.openligadb.de/getcurrentgroup/bl1"

    # Daten abrufen
    response_current_matchday = requests.get(url_current_matchday)
    data_current_matchday= response_current_matchday.json()

    df_current_matchday= pd.json_normalize(data_current_matchday)

    current_matchday_name, current_matchday_number = df_current_matchday.iloc[0, 0:2]

    
    response = {'current_matchday_name' : current_matchday_name,
                'current_matchday_number' : int(current_matchday_number)}
    return response

