# Diese Methode holt alle Dialoge (Frage - Antwort) zu einer schon bestehenden Unterhaltung über die conversation_id
def get_conversations_dialogs(conversation_id: str):
    from MongoDB_Connection import create_Mongodb_connection

    collection = create_Mongodb_connection()
    
    conv = collection.find_one({"conversation_id": conversation_id}, {"dialog": 1, "_id": 0})

    conversations_dialogs = []

    if conv and "dialog" in conv:
        conversations_dialogs = [
            {
                "question": entry.get("question"),
                "answer": entry.get("answer"),
                "date": entry.get("date"),
                "time": entry.get("time"),
            }
            for entry in conv["dialog"]
        ]

    return {"conversations_dialogs": conversations_dialogs}
