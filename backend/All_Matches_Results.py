# Diese Methode holt Informationen aus der API zu allen Spielergebnissen in der 1. Bundesliag im Saison 2024/25
# Da die Saison jetzt zu ende ist, wurde ein Anker gesetzt, nach diesem Anker (31.12.2024) werden die Daten so manipuliert, als wären sie noch offen
def fetch_all_matches_results() -> dict:
    import requests
    import pandas as pd
    import numpy as np
    import Current_Matchday
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()


    # API-Endpunkt für die Bundesliga-Tabelle
    url_matches_results = f"https://api.openligadb.de/getmatchdata/bl1/2024"

    # Daten abrufen
    response_matches_results = requests.get(url_matches_results)
    data_matches_results = response_matches_results.json()
    df_matches_results = pd.json_normalize(data_matches_results)
    df_matches_goals = df_matches_results



    # *************************************************
    # *************************************************
    # *************************************************

    # TEIL 1 START
    ######
    ######
    ######
    # Infos zu den Teams (Namen und Icons) und Spielen
    ######
    ######
    ######
    needed_columns = ['matchDateTime', 'group.groupName','matchIsFinished', 'team1.teamName', 'team2.teamName']

    df_matches_results = df_matches_results.loc[:, needed_columns]

    df_matches_results.columns = [
                        "Spiel-Datum und -Zeit",
                        "Spieltagname",
                        "Spiel beendet (bool)",
                        "Team 1 Name",
                        "Team 2 Name"
                    ]


    # TEIL 1 ENDE
    ######
    ######
    ######
    # Infos zu den Teams (Namen und Icons) und Spielen
    ######
    ######
    ######

    # *************************************************
    # *************************************************
    # *************************************************

    # TEIL 2 START
    ######
    ######
    ######
    # Halbzeit und Endzeit Ergebnisse
    ######
    ######
    ######

    df_matches_goals = pd.json_normalize(df_matches_goals['matchResults'])


    df_matches_goals.columns = ['halftime','finaltime']




    df_matches_goals = pd.json_normalize(df_matches_goals['finaltime']).add_prefix('finaltime_')



    df_matches_goals_needed_columns  = ['finaltime_pointsTeam1','finaltime_pointsTeam2']

    df_matches_goals = df_matches_goals.loc[:, df_matches_goals_needed_columns]

    df_matches_goals.columns = [
                                "Endergebnis Team 1",
                                "Endergebnis Team 2"
                            ]


    # TEIL 2 ENDE
    ######
    ######
    ######
    # Halbzeit und Endzeit Ergebnisse
    ######
    ######
    ######

    # *************************************************
    # *************************************************
    # *************************************************

    # TEIL 3 START
    ######
    ######
    ######
    # Weitere ETL-Schritte
    ######
    ######
    ######

    df_matches_info = pd.concat([df_matches_results,df_matches_goals],axis=1)

    # Neue Spalten für Datum und Zeit extrahieren
    df_matches_info['Spiel-Datum und -Zeit'] = pd.to_datetime(df_matches_info['Spiel-Datum und -Zeit'])
    df_matches_info.insert(2, 'Datum', df_matches_info['Spiel-Datum und -Zeit'].dt.date)
    df_matches_info.insert(3, 'Zeit', df_matches_info['Spiel-Datum und -Zeit'].dt.time)

    # DUMMY LÖSCHEN TESTEN AB HIER
    # DUMMY LÖSCHEN TESTEN AB HIER
    # DUMMY LÖSCHEN TESTEN AB HIER
    # DUMMY LÖSCHEN TESTEN AB HIER
    # DUMMY LÖSCHEN TESTEN AB HIER
    # DUMMY LÖSCHEN TESTEN AB HIER
    df_matches_info['Spiel beendet (bool)'] = np.where(
        pd.to_datetime(df_matches_info['Datum']) < pd.Timestamp('2024-12-31'),
        True,
        False
    )

    df_matches_info['Endergebnis Team 1'] = np.where(
        pd.to_datetime(df_matches_info['Datum']) < pd.Timestamp('2024-12-31'),
        df_matches_info['Endergebnis Team 1'],
        None
    )

    df_matches_info['Endergebnis Team 2'] = np.where(
        pd.to_datetime(df_matches_info['Datum']) < pd.Timestamp('2024-12-31'),
        df_matches_info['Endergebnis Team 2'],
        None
    )



    # DUMMY LÖSCHEN TESTEN BIS HIER
    # DUMMY LÖSCHEN TESTEN BIS HIER
    # DUMMY LÖSCHEN TESTEN BIS HIER
    # DUMMY LÖSCHEN TESTEN BIS HIER
    # DUMMY LÖSCHEN TESTEN BIS HIER
    # DUMMY LÖSCHEN TESTEN BIS HIER

    df_matches_info['Anzahl der Tore'] = df_matches_info.loc[:,'Endergebnis Team 1'] + df_matches_info.loc[:,'Endergebnis Team 2']

    df_matches_info['Spielergebnis'] = df_matches_info['Endergebnis Team 1'].astype(str) + ':' + df_matches_info['Endergebnis Team 2'].astype(str)



    df_matches_info['Gewinner'] = np.where(
        df_matches_info['Endergebnis Team 1'] > df_matches_info['Endergebnis Team 2'],
        df_matches_info['Team 1 Name'],
        np.where(
            df_matches_info['Endergebnis Team 1'] < df_matches_info['Endergebnis Team 2'],
            df_matches_info['Team 2 Name'],
             np.where(
                df_matches_info['Endergebnis Team 1'] == df_matches_info['Endergebnis Team 2'],
                'Unentschieden',
                None
            )
        )
    )

    df_matches_info['Team 1 Punkte'] = np.where(
        df_matches_info['Endergebnis Team 1'] > df_matches_info['Endergebnis Team 2'],
        3,
        np.where(
            df_matches_info['Endergebnis Team 1'] < df_matches_info['Endergebnis Team 2'],
            0,
            np.where(
                df_matches_info['Endergebnis Team 1'] == df_matches_info['Endergebnis Team 2'],
                1,
                None
            )
        )
    )

    df_matches_info['Team 2 Punkte'] = np.where(
        df_matches_info['Endergebnis Team 1'] > df_matches_info['Endergebnis Team 2'],
        0,
        np.where(
            df_matches_info['Endergebnis Team 1'] < df_matches_info['Endergebnis Team 2'],
            3,
            np.where(
                df_matches_info['Endergebnis Team 1'] == df_matches_info['Endergebnis Team 2'],
                1,
                None
            )
        )
    )



    # Spalte 'Spiel-Datum und -Zeit' löschen
    df_matches_info = df_matches_info.drop(columns=['Spiel-Datum und -Zeit'])

    # Spieltag Nummer

    df_matches_info.insert(1, 'Spieltagnummer', df_matches_info['Spieltagname'].str.extract(r'(\d+)\.').astype(int))


    # Hole den aktuellen Spieltag
    current_matchday_name = Current_Matchday.fetch_current_matchday().get('current_matchday_name')
    current_matchday_number = Current_Matchday.fetch_current_matchday().get('current_matchday_number')
    df_matches_info.insert(2, 'Spieltag Aktualität',
     np.where(
        current_matchday_number == df_matches_info['Spieltagnummer'],
        'Aktueller Spieltag',
        np.where(
            current_matchday_number  + 1 == df_matches_info['Spieltagnummer'] ,
            'Nächster Spieltag',
            np.where(
                current_matchday_number < df_matches_info['Spieltagnummer'],
                'Zukünftiger Spieltag',
                np.where(
                    current_matchday_number > df_matches_info['Spieltagnummer'],
                    'Vergangener Spieltag',
                    None
                ))
        )
    ))




    # TEIL 3 ENDE
    ######
    ######
    ######
    # Weitere ETL-Schritte
    ######
    ######
    ######

    # *************************************************
    # *************************************************
    # *************************************************


    description = """Diese Datenquelle (df_TYPE_EN_matches_results) enthält folgende Informationen für TYPE_DE:
                        - Name des Spieltages (Spaltenname: Spieltagname)
                        - Nummer des Spieltages (Spaltenname: Spieltagnummer)
                        - Datum des Spiels (Spaltenname: Datum)
                        - Uhrzeit des Spiels (Spaltenname: Zeit)
                        - Spielstatus, ob das Spiel beendet ist (boolescher Wert, Spaltenname: Spiel beendet)
                        - Name des ersten Teams (Spaltenname: Team 1 Name)
                        - Name des zweiten Teams (Spaltenname: Team 2 Name)
                        - Endergebnis des ersten Teams (Spaltenname: Endergebnis Team 1)
                        - Endergebnis des zweiten Teams (Spaltenname: Endergebnis Team 2)
                        - Anzahl der insgesamt erzielten Tore (Spaltenname: Anzahl der Tore)
                        - Ergebnis des Spiels als Text (Spaltenname: Spielergebnis)
                        - Gewinner des Spiels (Spaltenname: Gewinner)
                        - Punkte für Team 1 (Spaltenname: Team 1 Punkte)
                        - Punkte für Team 2 (Spaltenname: Team 2 Punkte)
                    """

    response = {'df_matches_results': df_matches_info,
                'description': description}
    
   

    return response