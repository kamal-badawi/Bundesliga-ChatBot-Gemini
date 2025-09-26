# Diese Methode erstellt mithilfe von Gemini einen Titel zu dem ersten Frage-Antwort-Paar einer neuen Unterhaltung
# Wichtiger Hinweis: Das Prompt wurde mit ChatGPT verbessert
# Die Fehler (Exception wurden mit ChatGPT erstellt)
def create_conversation_title_gemini(questions_and_answers) -> str:
    import google.generativeai as genai
    from decouple import config
    import time

    API_KEY = config("GOOGLE_GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)

    prompt = f"""
    Du bist ein datenbasierter Assistent mit fundierter Expertise in der 1. Fußball-Bundesliga.

    Dir werden Fragen und Antworten vorgelegt, die zuvor an ein Sprachmodell gestellt wurden: {questions_and_answers}

    Deine Aufgabe:  
    Formuliere einen prägnanten, sachlichen Titel, der den Inhalt der Fragen und Antworten treffend zusammenfasst.

    Vorgaben:
    - 2 bis 4 Wörter
    - Klar, verständlich und inhaltlich korrekt
    - Keine Wertungen, Zusätze oder Sonderzeichen
    - Gib nur den Titel als einzeiligen Fließtext aus - nichts weiter
    """

    model = genai.GenerativeModel("gemini-2.5-pro")
    max_retries = 3
    retry_delay = 60

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            
            title = response.text.strip()
            if not title:
                raise ValueError("Empty title received from Gemini")
            return title  
        except Exception as e:
            if attempt == max_retries - 1:
                
                return "Bundesliga-Diskussion"
            time.sleep(retry_delay)