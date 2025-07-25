# Pandas Anzeigeoptionen anpassen
# Sehr wichtig für ETL-Prozess
def get_pandas_Settings():
    import pandas as pd


    pd.set_option('display.max_columns', None) 
    pd.set_option('display.width', None)  
    pd.set_option('display.max_colwidth', None)  
    pd.set_option('display.max_rows', 500)  
