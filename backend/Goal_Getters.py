# Diese Methode holt Informationen aus der API zu Torschützen in der 1. Bundesliag im Saison 2025/26

def fetch_goal_getters() -> dict:
    import requests
    import sqlite3
    import pandas as pd
    import Pandas_Settings

    # Pandas Anzeigeoptionen anpassen
    Pandas_Settings.get_pandas_Settings()


    # Erstelle eine Datenbank-Tabelle (goal_getters)
    def create_goal_getters_database_table():
        connection = sqlite3.connect(r'APIs-Backup/goal_getters.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_getters (
                "index" INTEGER PRIMARY KEY AUTOINCREMENT,
                goalGetterId       INTEGER,
                goalGetterName      TEXT,
                goalCount     INTEGER
                
            )
        ''')

        connection.commit()
        return connection
    

    # Daten aus der API in der Datenbank speichern
    def create_api_data_backup(connection, df):
        """
        Löscht alte Daten in goal_getters und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor = connection.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols = ['goalGetterName', 'goalCount']
        
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
        cursor.execute("DELETE FROM goal_getters")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols))
        insert_sql = f"INSERT INTO goal_getters ({', '.join(desired_cols)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor.executemany(insert_sql, rows)
        connection.commit()
        return len(rows)
    


    try:

        # API-Endpunkt für die Bundesliga-Tabelle
        url_goal_getters = "https://api.openligadb.de/getgoalgetters/bl1/2025"

        # Daten abrufen
        response_goal_getters  = requests.get(url_goal_getters)
        data_goal_getters = response_goal_getters.json()

        # In DataFrame umwandeln
        df_goal_getters = pd.json_normalize(data_goal_getters)
       
        

        # DB + Tabelle sicherstellen
        conn = create_goal_getters_database_table()
        # Daten einfügen
        n_inserted = create_api_data_backup(conn, df_goal_getters)
                                            
        

    
    except Exception as e:
        # DB Fallback
        conn = sqlite3.connect(r'APIs-Backup/goal_getters.db')
        df_goal_getters = pd.read_sql_query("SELECT * FROM goal_getters", conn)
       
       

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn.close()

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




