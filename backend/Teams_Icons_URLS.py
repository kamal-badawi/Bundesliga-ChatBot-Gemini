# Diese Methode holt Icons (Logos) aus der API zu den vorhandenen Teams in der 1. Bundesliag im Saison 2025/26
def fetch_teams_icons_urls() -> dict:
    import requests
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()

    # API-Endpunkt für die Bundesliga-Tabelle
    url_teams_icons_urls = "https://api.openligadb.de/getbltable/bl1/2025"

    # Daten abrufen
    response_teams_icons_urls = requests.get(url_teams_icons_urls)
    data_teams_icons_urls = response_teams_icons_urls.json()

    # In DataFrame umwandeln
    df_teams_icons_urls = pd.json_normalize(data_teams_icons_urls)



    needed_columns = [ 'teamName', 'teamIconUrl']


    df_teams_icons_urls = df_teams_icons_urls.loc[:, needed_columns]

    # Spaltennamen ins Deutsche übersetzen, um eine höhere Genauigkeit des LLM zu sorgen
    german_needed_columns = [
            'Teamname',
            'Team-Icon-URL']

    df_teams_icons_urls.columns = german_needed_columns

    description = """Diese Datenquelle (df_teams_icons_urls) enthält folgende Informationen:
                - Name jedes Teams (Spaltenname: Teamname)
                - Icon als URL für jedes Team (Spaltenname: Team-Icon-URL)
                """
    
 
    response = {'df_teams_icons_urls':df_teams_icons_urls,
                'description':description}
        
    return response


