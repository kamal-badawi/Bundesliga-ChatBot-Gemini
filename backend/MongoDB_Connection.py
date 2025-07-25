# Diese Methode erstellt eine Verbnidung zur MongoDB Datenbank
def create_Mongodb_connection():
    from pymongo import MongoClient
    from decouple import config

    db_password = config("MONGO_DB_PASSWORD")
    db_user = config("MONGO_DB_USERNAME")
    uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.25aidov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['bundesligachatbot']
    collection = db['chathistory']


    return collection
