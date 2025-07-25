# Diese Methode wird genutzt, um ein Frage-Antwort-Paar an eine schon bestehende Unterhaltung hinzuzufügen
# Die Fehler-Möglichkeiten wurden durch ChatGPT erzeuget
def add_dialog_item(user_id: str, conversation_id: str, question: str, answer: str, date: str, time: str) -> bool:
    from MongoDB_Connection import create_Mongodb_connection
    collection = create_Mongodb_connection()
    
    new_entry = {
        "question": question,
        "answer": answer,
        "date": date,
        "time": time
    }

    try:
       
        result = collection.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$push": {"dialog": new_entry}},
            upsert=False 
        )
        
        if result.matched_count == 0:
            print(f"Keine Conversation gefunden für user_id: {user_id}, conversation_id: {conversation_id}")
            return False
            
        return result.modified_count > 0
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Dialog-Items: {str(e)}")
        return False