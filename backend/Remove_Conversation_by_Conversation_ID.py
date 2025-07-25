
# Diese Methode wird genutzt, um eine Unterhaltung über die conversation_id zu löschen
def remove_conversation_by_conversation_id(conversation_id: str) -> bool:
    from MongoDB_Connection import create_Mongodb_connection

    collection = create_Mongodb_connection()
    
    result = collection.delete_one({"conversation_id": conversation_id})
    
    
    if result.deleted_count == 0:
        return False  
    return True  
