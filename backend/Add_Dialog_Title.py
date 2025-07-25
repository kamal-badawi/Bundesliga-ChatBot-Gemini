# Diese Methode wird genutzt, um einen Titel an eine neue Unterhaltung hinzuzufügen
# Der Titel wird durch Gemini in einer anderen Methoden anhand der ersten Frage und Antwort erstellt
def add_dialog_title(user_id: str, conversation_id: str, title: str) -> bool:
    from MongoDB_Connection import create_Mongodb_connection

    collection = create_Mongodb_connection()

   
    result = collection.update_one(
        {"user_id": user_id, "conversation_id": conversation_id},
        {"$set": {"title": title}}
    )

    
    return result.modified_count > 0
