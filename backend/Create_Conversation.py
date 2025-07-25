# Diese Methode erstellt eine neue Unterhaltung (New)
def create_conversation(user_id: str, conversation_id: str, title: str, dialog: list) -> bool:
    from MongoDB_Connection import create_Mongodb_connection
    from datetime import datetime

    collection = create_Mongodb_connection()
    
    
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")

    
    existing = collection.find_one({"user_id": user_id, "conversation_id": conversation_id})
    if existing:
        return False 

    
    new_doc = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "title": title,
        "date": date,
        "time": time,
        "dialog": dialog
    }
    
    try:
        collection.insert_one(new_doc)
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen der Konversation: {str(e)}")
        return False