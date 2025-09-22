# Diese Methode holt Informationen aus der API zu allen Spielergebnissen in der 1. Bundesliag im Saison 2025/26
def fetch_all_matches_results() -> dict:
    import requests
    import sqlite3
    import pandas as pd
    import numpy as np
    import Current_Matchday
    import Pandas_Settings
    from decouple import config

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()

    
    # Datenquelle (APIs)
    DATA_SOURCE = config("DATA_SOURCE")
    
    # Erstelle eine Datenbank-Tabelle (match_results)
    def create_match_results_database_table():
        connection = sqlite3.connect(r'APIs-Backup/match_results.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS match_results (
                "index" INTEGER PRIMARY KEY AUTOINCREMENT,
                matchDateTime TEXT,
                "group_groupName" TEXT,
                matchIsFinished INTEGER,
                "team1_teamName" TEXT,
                "team2_teamName" TEXT,
                finaltime_pointsTeam1 REAL,
                finaltime_pointsTeam2 REAL
            )
        ''')

        connection.commit()
        return connection
    

    # Daten aus der API in der Datenbank speichern
    def create_api_data_backup(connection, df):
        """
        Löscht alte Daten in match_results und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor = connection.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols = ['matchDateTime', 'group_groupName', 'matchIsFinished', 'team1_teamName',
       'team2_teamName', 'finaltime_pointsTeam1', 'finaltime_pointsTeam2']
        
        
        # drop 'index', falls vom DataFrame vorhanden
        if 'index' in df.columns:
            df = df.drop(columns=['index'])
        
        # Spalten mappen / fehlende Spalten mit None füllen
        mapped = {}
        for col in desired_cols:
            if col in df.columns:
                mapped[col] = df[col]
            else:
                mapped[col] = pd.Series([None] * len(df), index=df.index)
        df_insert = pd.DataFrame(mapped, columns=desired_cols)
        df_insert = df_insert.where(pd.notnull(df_insert), None)  # NaN -> None

        # Alte Daten löschen
        cursor.execute("DELETE FROM match_results")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols))
        insert_sql = f"INSERT INTO match_results ({', '.join(desired_cols)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor.executemany(insert_sql, rows)
        connection.commit()
        return len(rows)
    

    try:
        # API-Endpunkt für die Bundesliga-Tabelle
        url_matches_results = f"https://{DATA_SOURCE}/getmatchdata/bl1/2025"

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
        # Halbzeit und Endzeit Ergebnisse
        ######
        ######
        ######

        df_matches_goals = pd.json_normalize(df_matches_goals['matchResults'])


        df_matches_goals.columns = ['halftime','finaltime']




        df_matches_goals = pd.json_normalize(df_matches_goals['finaltime']).add_prefix('finaltime_')



        df_matches_goals_needed_columns  = ['finaltime_pointsTeam1','finaltime_pointsTeam2']

        df_matches_goals = df_matches_goals.loc[:, df_matches_goals_needed_columns]

        

        


        # TEIL 1 ENDE
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

        # TEIL 2 START
        ######
        ######
        ######
        # Infos zu den Teams (Namen und Icons) und Spielen
        ######
        ######
        ######
        needed_columns = ['matchDateTime', 'group.groupName','matchIsFinished', 'team1.teamName', 'team2.teamName']

        df_matches_results = df_matches_results.loc[:, needed_columns]

        

        # TEIL 2 ENDE
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

        # TEIL 3 START
        ######
        ######
        ######
        # Weitere ETL-Schritte
        ######
        ######
        ######

        
        df_matches_info = pd.concat([df_matches_results,df_matches_goals],axis=1)
        
        
        # DB + Tabelle sicherstellen
        conn = create_match_results_database_table()

        needed_columns = ['matchDateTime', 'group_groupName', 'matchIsFinished', 'team1_teamName',
                          'team2_teamName','finaltime_pointsTeam1', 'finaltime_pointsTeam2']
        df_matches_info.columns = needed_columns
        # Daten einfügen
       
        n_inserted = create_api_data_backup(conn, df_matches_info)


    
    except Exception as e: 
        print(e)
        # DB Fallback
        conn = sqlite3.connect(r'APIs-Backup/match_results.db')
        df_matches_info = pd.read_sql_query("SELECT matchDateTime, group_groupName, matchIsFinished, team1_teamName, team2_teamName, finaltime_pointsTeam1, finaltime_pointsTeam2 FROM match_results", conn)
        
        
    

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn.close()

    
    
    
    
    df_matches_info.columns = [
                        "Spiel-Datum und -Zeit",
                        "Spieltagname",
                        "Spiel beendet (bool)",
                        "Team 1 Name",
                        "Team 2 Name",
                        "Endergebnis Team 1",
                        "Endergebnis Team 2"
                          ]

    # Neue Spalten für Datum und Zeit extrahieren
    df_matches_info['Spiel-Datum und -Zeit'] = pd.to_datetime(df_matches_info['Spiel-Datum und -Zeit'])
    df_matches_info.insert(2, 'Datum', df_matches_info['Spiel-Datum und -Zeit'].dt.date)
    df_matches_info.insert(3, 'Zeit', df_matches_info['Spiel-Datum und -Zeit'].dt.time)

    

    df_matches_info['Anzahl der Tore'] = df_matches_info.loc[:,'Endergebnis Team 1'] + df_matches_info.loc[:,'Endergebnis Team 2']

    df_matches_info['Spielergebnis'] = (
    df_matches_info['Endergebnis Team 1']
        .astype(str)
        .str.split('.')
        .str[0]
        .where(df_matches_info['Endergebnis Team 1'].notna())
    + ':' +
    df_matches_info['Endergebnis Team 2']
        .astype(str)
        .str.split('.')
        .str[0]
        .where(df_matches_info['Endergebnis Team 2'].notna()))

    


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





