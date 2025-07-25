# Diese Methode holt Informationen aus der API zu Torschützen in der 1. Bundesliag im Saison 2024/25

def fetch_goal_getters() -> dict:
    import requests
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()

    # API-Endpunkt für die Bundesliga-Tabelle
    url_goal_getters = "https://api.openligadb.de/getgoalgetters/bl1/2024"

    # Daten abrufen
    response_goal_getters  = requests.get(url_goal_getters)
    data_goal_getters = response_goal_getters.json()


    # In DataFrame umwandeln
    df_goal_getters = pd.json_normalize(data_goal_getters)

    needed_columns = ['goalGetterName', 'goalCount']

    df_goal_getters = df_goal_getters.loc[:, needed_columns]

    # Spaltennamen ins Deutsche übersetzen, um eine höhere Genauigkeit des LLM zu sorgen
    german_needed_columns = ['Spielername',
        'Anzahl der Tore']

    df_goal_getters.columns = german_needed_columns




    description = """Diese Datenquelle (df_goal_getters) enthält folgende Informationen:
                    - Spielername  (Spaltenname: Spielername)
                    - Anzahl der Tore in aller Spiele  (Spaltenname: Anzahl der Tore)
                """

    response = {'df_goal_getters': df_goal_getters,
                        'description': description}

    return response