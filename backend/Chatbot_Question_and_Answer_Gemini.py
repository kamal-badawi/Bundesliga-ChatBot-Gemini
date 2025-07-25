# Wichtiger Hinweis: Das Prompt wurde mit ChatGPT verbessert
def get_chatbot_question_and_answer_gemini(source, information, question) -> dict:
    import google.generativeai as genai
    from RAG import dataframes_to_documents, build_vectorstore, retrieve_relevant_context
    from decouple import config

    
    API_KEY = config("GOOGLE_GEMINI_API_KEY")


    genai.configure(api_key=API_KEY)

   
    documents = dataframes_to_documents(source)
    # print('documents: ',documents)

   
    vectordb = build_vectorstore(documents)
    # print('vectordb: ',vectordb)

    
    relevant_context = retrieve_relevant_context(question, vectordb)
    # print('relevant_context: ',relevant_context)

    
    prompt = f"""
    Du bist ein datenbasierter Assistent mit ausgewiesener Expertise in der 1. Fußball-Bundesliga.

    Dir stehen zwei strukturierte Ressourcen zur Verfügung:
    1. Kontext: Auszug aus Bundesliga-Datenquellen, automatisch gefiltert:
    {relevant_context}

    2. Übersicht über die Datenstruktur:
    {information}

    Aufgabe:
    Beantworte folgende Frage ausschließlich basierend auf den oben genannten Kontextdaten:
    {question}

    Verhaltensregeln:
    - Wenn die verfügbaren Daten keine fundierte Antwort ermöglichen, gib exakt diesen Satz zurück: "Ich habe keine Informationen dazu."
    - Die Antwort muss sachlich, präzise und leicht verständlich formuliert sein.
    - Verweise bei Bedarf auf konkrete Werte oder Statistiken aus dem Kontext.
    - Gib keine Informationen zurück, die nicht im Kontext enthalten sind.
    - Die Ausgabe muss ein einzeiliger Fließtext sein - ohne Zeilenumbrüche oder unnötige Ausschmückungen.
    """

    # Schritt 5: Anfrage an Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        import time
        time.sleep(60)
        response = model.generate_content(prompt)

    return {"text": response.text}