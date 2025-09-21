# Diese Methode holt Informationen aus der API zur Tabelle in der 1. Bundesliag im Saison 2025/26
def fetch_bundesliga_table() -> dict:
    import requests
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()

    # API-Endpunkt für die Bundesliga-Tabelle
    url_bundesliga_table = "https://api.openligadb.de/getbltable/bl1/2025"

    # Daten abrufen
    response_bundesliga_table = requests.get(url_bundesliga_table)
    data_bundesliga_table = response_bundesliga_table.json()

    # In DataFrame umwandeln
    df_bundesliga_table = pd.json_normalize(data_bundesliga_table)
    df_bundesliga_table = df_bundesliga_table.reset_index()
    df_bundesliga_table.loc[:,'rank']  = df_bundesliga_table.loc[:,'index'] + 1


    
    needed_columns = ['rank', 'teamName',  'points',
                      'opponentGoals', 'goals', 'matches', 'won', 'lost', 'draw', 'goalDiff']


    df_bundesliga_table = df_bundesliga_table.loc[:, needed_columns]

    # Spaltennamen ins Deutsche übersetzen, um eine höhere Genauigkeit des LLM zu sorgen
    german_needed_columns = [
    'Tabellenplatz',
    'Teamname',
    'Punkte',
    'Gegentore',
    'Tore',
    'Spiele',
    'Siege',
    'Niederlagen',
    'Unentschieden',
    'Tordifferenz']

    df_bundesliga_table.columns = german_needed_columns

    description = """Diese Datenquelle (df_bundesliga_table) enthält folgende Informationen:
                - Tabellenplatz jedes Teams in der Bundesliga (Spaltenname: Tabellenplatz)
                - Name jedes Teams (Spaltenname: Teamname)
                - Anzahl der bisher erzielten Punkte (Spaltenname: Punkte)
                - Anzahl der kassierten Gegentore (Spaltenname: Gegentore)
                - Anzahl der erzielten Tore (Spaltenname: Tore)
                - Anzahl der bisher absolvierten Spiele (Spaltenname: Spiele)
                - Anzahl der gewonnenen Spiele (Spaltenname: Siege)
                - Anzahl der verlorenen Spiele (Spaltenname: Niederlagen)
                - Anzahl der unentschiedenen Spiele (Spaltenname: Unentschieden)
                - Tordifferenz (Tore minus Gegentore) (Spaltenname: Tordifferenz)
            """

    
    
    response = {'df_bundesliga_table': df_bundesliga_table,
                        'description': description}

    return response


