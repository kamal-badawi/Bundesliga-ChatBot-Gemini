# Diese Methode holt Informationen aus der API zu den vorhandenen Teams in der 1. Bundesliag im Saison 2025/26
def fetch_all_bundesliga_teams():
    import requests
    import sqlite3
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen, um alle Spalten anzuzuegen
    Pandas_Settings.get_pandas_Settings()


    # Erstelle eine Datenbank-Tabelle (bundesliga_table)
    def create_available_teams_database_table():
        connection = sqlite3.connect(r'APIs-Backup/available_teams.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS available_teams (
                "index" INTEGER PRIMARY KEY AUTOINCREMENT,
                teamName     INTEGER,
                shortName       TEXT,
                teamIconUrl      TEXT,
                teamGroupName    TEXT
                
            )
        ''')

        connection.commit()
        return connection
    

    # Daten aus der API in der Datenbank speichern
    def create_api_data_backup(connection, df):
        """
        Löscht alte Daten in available_teams und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor = connection.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols = [
            'teamName'
        ]
        
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
        cursor.execute("DELETE FROM available_teams")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols))
        insert_sql = f"INSERT INTO available_teams ({', '.join(desired_cols)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor.executemany(insert_sql, rows)
        connection.commit()
        return len(rows)
    

    try:
        # API-Endpunkt für die Available-Teams
        all_bundesliga_teams = "https://api.openligadb.de/getavailableteams/bl1/2025"

        # Daten werden abrgerufen
        response_all_bundesliga_teams = requests.get(all_bundesliga_teams)
        data_all_bundesliga_teams = response_all_bundesliga_teams.json()


        # In DataFrame umwandeln
        df_all_bundesliga_teams = pd.json_normalize(data_all_bundesliga_teams)

        # DB + Tabelle sicherstellen
        conn = create_available_teams_database_table()

        # Daten einfügen
        n_inserted = create_api_data_backup(conn, df_all_bundesliga_teams)
        
    except Exception as e:
        # DB Fallback
        conn = sqlite3.connect(r'/APIs-Backup/available_teams.db')
        df_all_bundesliga_teams = pd.read_sql_query("SELECT * FROM available_teams", conn)
       

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn.close()

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

