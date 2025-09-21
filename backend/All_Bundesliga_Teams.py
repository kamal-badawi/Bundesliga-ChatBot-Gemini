# Diese Methode holt Informationen aus der API zu den vorhandenen Teams in der 1. Bundesliag im Saison 2025/26
def fetch_all_bundesliga_teams():
    import requests
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen, um alle Spalten anzuzuegen
    Pandas_Settings.get_pandas_Settings()

    # API-Endpunkt für die Bundesliga-Tabelle
    all_bundesliga_teams = "https://api.openligadb.de/getavailableteams/bl1/2025"

    # Daten werden abrgerufen
    response_all_bundesliga_teams = requests.get(all_bundesliga_teams)
    data_all_bundesliga_teams = response_all_bundesliga_teams.json()


    # In DataFrame umwandeln
    df_all_bundesliga_teams = pd.json_normalize(data_all_bundesliga_teams)

    needed_columns = [ 'teamName']

    df_all_bundesliga_teams = df_all_bundesliga_teams.loc[:, needed_columns]

    # Spaltennamen ins Deutsche übersetzen, um eine höhere Genauigkeit des LLM zu sorgen
    german_needed_columns = ['Teamname']

    df_all_bundesliga_teams.columns = german_needed_columns




    description = """Diese Datenquelle (df_all_bundesliga_teams) enthält folgende Informationen:
            - Auflistung aller Teams in der Bundesliga (Spaltenname: Teamname)
        """


    
    response = {'df_all_bundesliga_teams': df_all_bundesliga_teams,
                    'description': description}

    return response

