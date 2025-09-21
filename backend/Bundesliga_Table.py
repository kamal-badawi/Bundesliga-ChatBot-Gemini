# Diese Methode holt Informationen aus der API zur Tabelle in der 1. Bundesliag im Saison 2025/26
def fetch_bundesliga_table() -> dict:
    import requests
    import sqlite3
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()


    # Erstelle eine Datenbank-Tabelle (bundesliga_table)
    def create_bundesliga_table_database_table():
        connection = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bundesliga_table (
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
        Löscht alte Daten in bundesliga_table und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor = connection.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols = [
            'teamInfoId', 'teamName', 'shortName', 'teamIconUrl',
            'points', 'opponentGoals', 'goals', 'matches',
            'won', 'lost', 'draw', 'goalDiff'
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
        cursor.execute("DELETE FROM bundesliga_table")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols))
        insert_sql = f"INSERT INTO bundesliga_table ({', '.join(desired_cols)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor.executemany(insert_sql, rows)
        connection.commit()
        return len(rows)

    # -------------------------
    # Haupt-Logik: API abrufen / DB Fallback
    # -------------------------
    try:
        # API-Daten abrufen
        url = "https://api.openligadb.de/getbltable/bl1/2025"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # In DataFrame umwandeln
        df_bundesliga_table = pd.json_normalize(data).reset_index()

        # DB + Tabelle sicherstellen
        conn = create_bundesliga_table_database_table()

        # Daten einfügen
        n_inserted = create_api_data_backup(conn, df_bundesliga_table)

    except Exception as e:
        # DB Fallback
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        df_bundesliga_table = pd.read_sql_query("SELECT * FROM bundesliga_table", conn)
       

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn.close()

        

    
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


