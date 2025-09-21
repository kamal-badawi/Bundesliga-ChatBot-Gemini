# Gibt den Namen und die Nummer des aktuellen Bundesligaspieltags zurück
def fetch_current_matchday() -> dict:
    import requests
    import sqlite3
    import pandas as pd



    # Erstelle eine Datenbank-Tabelle (current_match_day)
    def create_current_match_day_database_table():
        connection_CMD = sqlite3.connect(r'APIs-Backup/current_match_day.db')
        cursor_CMD = connection_CMD.cursor()

        cursor_CMD.execute('''
            CREATE TABLE IF NOT EXISTS current_match_day (
                "index" INTEGER PRIMARY KEY AUTOINCREMENT,
                groupName       TEXT,
                groupOrderID      INTEGER,
                groupID     INTEGER
                
            )
        ''')

        connection_CMD.commit()
        return connection_CMD
    

    # Daten aus der API in der Datenbank speichern
    def create_api_data_backup_CMD(connection_CMD, df):
        """
        Löscht alte Daten in current_match_day und fügt neue Zeilen ein.
        Schema bleibt erhalten (AUTOINCREMENT "index" bleibt).
        """
        cursor_CMD = connection_CMD.cursor()
        
        # gewünschte Spalten in der DB
        desired_cols_CMD = [
            'groupName', 'groupOrderID', 'groupID'
        ]
        
        # drop 'index', falls vom DataFrame vorhanden
        if 'index' in df.columns:
            df = df.drop(columns=['index'])
        
        # Spalten mappen / fehlende Spalten mit None füllen
        mapped = {}
        for col in desired_cols_CMD:
            if col in df.columns:
                mapped[col] = df[col]
            else:
                mapped[col] = pd.Series([None] * len(df), index=df.index)
        df_insert = pd.DataFrame(mapped, columns=desired_cols_CMD)
        df_insert = df_insert.where(pd.notnull(df_insert), None)  # NaN -> None

        # Alte Daten löschen
        cursor_CMD.execute("DELETE FROM current_match_day")

        # Bulk Insert
        placeholders = ",".join(["?"] * len(desired_cols_CMD))
        insert_sql = f"INSERT INTO current_match_day ({', '.join(desired_cols_CMD)}) VALUES ({placeholders})"
        rows = [tuple(row) for row in df_insert.itertuples(index=False, name=None)]
        
        if rows:
            cursor_CMD.executemany(insert_sql, rows)
        connection_CMD.commit()
        return len(rows)
    



    
    try:

        # API-Endpunkt für den aktuellen Spieltag
        url_current_matchday = "https://api.openligadb.de/getcurrentgroup/bl1"

        # Daten abrufen
        response_current_matchday = requests.get(url_current_matchday)
        data_current_matchday= response_current_matchday.json()
        
        df_current_matchday = pd.json_normalize(data_current_matchday)
        # Spalten umbenennen auf die erwarteten DB-Spalten
        df_current_matchday = df_current_matchday.rename(columns={
            'GroupName': 'groupName',
            'GroupOrderID': 'groupOrderID',
            'GroupID': 'groupID'
        })
        
        
        current_matchday_name = df_current_matchday.at[0, 'groupName']
        current_matchday_number = int(df_current_matchday.at[0, 'groupOrderID'])

        # DB + Tabelle sicherstellen
        conn_CMD = create_current_match_day_database_table()
        # Daten einfügen
        n_inserted_CMD = create_api_data_backup_CMD(conn_CMD, df_current_matchday)

        
       

    except Exception as e:
        
        # DB Fallback
        conn_CMD = sqlite3.connect(r'APIs-Backup/current_match_day.db')
        df_current_matchday = pd.read_sql_query("SELECT groupName, groupOrderID FROM current_match_day", conn_CMD)
        current_matchday_name = df_current_matchday.iloc[0, df_current_matchday.columns.get_loc('groupName')]
        group_order_id_raw = df_current_matchday.iloc[0][df_current_matchday.columns.get_loc('groupOrderID')]
        current_matchday_number = int(group_order_id_raw)
       
       

    finally:
        # Verbindung schließen
        conn = sqlite3.connect(r'APIs-Backup/bundesliga_table.db')
        conn_CMD.close()

    
    

    
    response = {'current_matchday_name' : current_matchday_name,
                'current_matchday_number' : current_matchday_number}
  
    
    return response



