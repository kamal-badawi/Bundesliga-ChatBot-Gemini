# Diese Methode holt Icons (Logos) aus der API zu den vorhandenen Teams in der 1. Bundesliag im Saison 2025/26
def fetch_teams_icons_urls() -> dict:
    import requests
    import sqlite3
    import pandas as pd
    import Pandas_Settings
    from decouple import config

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()

    # Datenquelle (APIs)
    DATA_SOURCE = config("DATA_SOURCE")

    # Erstelle eine Datenbank-Tabelle (teams_icons_urls)
    def create_teams_icons_urls_database_table():
        connection = sqlite3.connect(r'APIs-Backup/teams_icons_urls.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams_icons_urls (
                "index" INTEGER PRIMARY KEY AUTOINCREMENT,
                teamInfoId     INTEGER,
                teamName       TEXT,
                shortName      TEXT,
                teamIconUrl    TEXT,
                points         INTEGER,
                opponentGoals  INTEGER,
                goals          INTEGER,
                matches        INTEGER,
                won            INTEGER,
                lost           INTEGER,
                draw           INTEGER,
                goalDiff       INTEGER
            )
        ''')

        connection.commit()
        return connection
    

     # Daten aus der API in der Datenbank speichern
    def create_api_data_backup(connection, df):
        """
        Löscht alte Daten in teams_icons_urls und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor = connection.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols = [ 'teamName', 'teamIconUrl']
        
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
        cursor.execute("DELETE FROM teams_icons_urls")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols))
        insert_sql = f"INSERT INTO teams_icons_urls ({', '.join(desired_cols)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor.executemany(insert_sql, rows)
        connection.commit()
        return len(rows)

    try:
        # API-Endpunkt für die Teams Icons Urls
        url_teams_icons_urls = f"https://{DATA_SOURCE}/getbltable/bl1/2025"

        # Daten abrufen
        response_teams_icons_urls = requests.get(url_teams_icons_urls)
        data_teams_icons_urls = response_teams_icons_urls.json()

        # In DataFrame umwandeln
        df_teams_icons_urls = pd.json_normalize(data_teams_icons_urls)

        # DB + Tabelle sicherstellen
        conn = create_teams_icons_urls_database_table()

        # Daten einfügen
        n_inserted = create_api_data_backup(conn, df_teams_icons_urls)
        


    except Exception as e:
        # DB Fallback
        conn = sqlite3.connect(r'APIs-Backup/teams_icons_urls.db')
        df_teams_icons_urls = pd.read_sql_query("SELECT * FROM teams_icons_urls", conn)
       

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn.close()

    needed_columns   = [ 'teamName', 'teamIconUrl']
    df_teams_icons_urls = df_teams_icons_urls.loc[:, needed_columns]

    
    german_needed_columns = [
            'Teamname',
            'Team-Icon-URL']

    # Spaltennamen ins Deutsche übersetzen, um eine höhere Genauigkeit des LLM zu sorgen
    

    df_teams_icons_urls.columns = german_needed_columns

    description = """Diese Datenquelle (df_teams_icons_urls) enthält folgende Informationen:
                - Name jedes Teams (Spaltenname: Teamname)
                - Icon als URL für jedes Team (Spaltenname: Team-Icon-URL)
                """
    

    response = {'df_teams_icons_urls':df_teams_icons_urls,
                'description':description}
    
    
    return response


