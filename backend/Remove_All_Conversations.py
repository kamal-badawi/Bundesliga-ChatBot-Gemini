
# Diese Methode wird genutzt, um Unterhaltungen eines Nutzers über die user_id zu löschen
def remove_all_conversations(user_id: str) -> bool:
    from MongoDB_Connection import create_Mongodb_connection

    collection = create_Mongodb_connection()
    
    result = collection.delete_many({"user_id": user_id})
    
    
    if result.deleted_count == 0:
        return False  
    return True