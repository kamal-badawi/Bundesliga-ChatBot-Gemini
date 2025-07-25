# Diese Methode holt alle Titel (mit Datum und Uhrzeit) zu einer bestehenden Unterhaltung über die user_id
def get_conversations_info(user_id):
    from MongoDB_Connection import create_Mongodb_connection

    collection = create_Mongodb_connection()
   
    
    conversations = collection.find(
        {"user_id": user_id},
        {"title": 1, "conversation_id": 1, "date": 1, "time": 1, "_id": 0}
    )

    
    conversations_info = []

    for conv in conversations:
        conversations_info.append({
            "title": conv.get("title"),
            "conversation_id": conv.get("conversation_id"),
            "date": conv.get("date"),
            "time": conv.get("time")
        })

    return conversations_info