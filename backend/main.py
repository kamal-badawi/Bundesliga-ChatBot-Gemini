# Wichtiger Hinweis: Die Doc-Strings wurden mit ChatGPT erstellt
from fastapi import FastAPI, UploadFile, File,  HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from Chatbot_Question_and_Answer_Gemini import get_chatbot_question_and_answer_gemini
from Text_to_Speech import run_text_to_speech
from Speech_to_Text import run_speech_to_text

from Conversations_Info import get_conversations_info
from Conversations_Dialogs import get_conversations_dialogs
from Remove_All_Conversations import remove_all_conversations
from Remove_Conversation_by_Conversation_ID import remove_conversation_by_conversation_id
from Create_Conversation import create_conversation
from Add_Dialog_Item import add_dialog_item
from Add_Dialog_Title import add_dialog_title
from Generate_Conversation_ID import generate_conversation_id
from Create_Conversation_Title_Gemini import create_conversation_title_gemini
import Create_PDF
import Send_Report_By_Email
import All_Data
import General_Information


app = FastAPI(version='1.0', title='Bundesliga-ChatBot')

# ORIGINS für das Frontend (React)
origins = ['http://localhost:5173',
           'http://localhost:5174',
           'http://localhost:4173',
           'http://localhost:4174',
           'http://localhost:4000',]

# CORS - Middlewares
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


@app.get("/")
async def read_root():
    """
    Root-Endpunkt zur Überprüfung, ob der Server aktiv ist.

    Returns:
        dict: Eine einfache JSON-Antwort mit einer Bestätigungsnachricht.
    """
    return {"message": "ROOT"}


class QuestionRequest(BaseModel):
    question: str
    last_question: str
    last_answer: str

@app.post("/question")
async def ask_question(request: QuestionRequest) -> dict:
    """
    Verarbeitet eine POST-Anfrage, um eine vom Benutzer gestellte Frage zu beantworten.

    Diese Endpoint-Funktion nimmt eine Frage sowie Kontext aus vorherigen Fragen/Antworten entgegen,
    sammelt allgemeine Informationen und Datenquellen, und übergibt diese an eine Chatbot-Funktion,
    die eine Antwort generiert. Die Antwort wird anschließend als JSON-Dictionary zurückgegeben.

    Args:
        request (QuestionRequest): Das Anfrageobjekt mit folgenden Feldern:
            - question (str): Die aktuell vom Benutzer gestellte Frage
            - last_question (str): Die vorherige Frage des Benutzers (für Kontext)
            - last_answer (str): Die vorherige Antwort des Systems (für Kontext)

    Returns:
        dict: Ein Dictionary mit der vom Chatbot generierten Antwort unter dem Schlüssel 'answer'.
              Beispiel: {'answer': 'Dies ist die generierte Antwort...'}
    """
    information = General_Information.get_general_information()
    source = All_Data.get_all_data()

    question = request.question
    last_question = request.last_question
    last_answer = request.last_answer
    response = get_chatbot_question_and_answer_gemini(source, information, question, last_question, last_answer)
    answer = response.get("text")
    return {'answer': answer}


class ConversationInfoRequest(BaseModel):
    user_id: str

@app.post("/conversations_info")
async def post_conversations_info(request: ConversationInfoRequest):
    """
    Lädt die Gesprächsinformationen eines Benutzers (Titel, ID, Datum, Uhrzeit).

    Parameter:
    - request (ConversationInfoRequest): Objekt mit der user_id.

    Ablauf:
    - Ruft die Funktion `get_conversations_info` mit der user_id auf.
    - Gibt eine 404-Fehlermeldung zurück, wenn keine Daten gefunden werden.
    - Gibt bei Erfolg eine Liste mit Gesprächsinformationen als JSON zurück.

    Rückgabewert:
    - Liste von Objekten mit 'title', 'conversation_id', 'date', 'time'.
    """
    data = get_conversations_info(request.user_id)

    if not data:
        raise HTTPException(status_code=404, detail="No conversations found")

    print('Conversation info has been retrieved')
    return {"conversations": data}


class DeleteAllConversationsRequest(BaseModel):
    user_id: str

@app.delete("/delete_all_conversations")
async def delete_all_conversations(request: DeleteAllConversationsRequest):
    """
    Löscht alle Konversationen eines bestimmten Benutzers.

    Parameter:
    - request (DeleteAllConversationsRequest): Objekt mit dem Feld user_id.

    Ablauf:
    - Ruft die Funktion `remove_all_conversations` auf, um alle Gespräche des angegebenen Benutzers zu löschen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn der Benutzer nicht existiert oder keine Konversationen zum Löschen vorhanden sind.
    - Gibt eine Bestätigung auf der Konsole aus und sendet eine Erfolgsnachricht zurück.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigung, dass alle Konversationen des Benutzers gelöscht wurden.
    """
    user_id = request.user_id
    success = remove_all_conversations(user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found or no conversations to delete")

    print(f'Conversations for {user_id} have been removed')
    return {'message': f'Conversations for {user_id} have been removed'}


class DeleteConversationByConversationIDRequest(BaseModel):
    conversation_id: str

@app.delete("/delete_conversation_by_conversation_id")
async def delete_conversation_by_conversation_id(request: DeleteConversationByConversationIDRequest):
    """
    Löscht eine spezifische Konversation basierend auf der conversation_id.

    Parameter:
    - request (DeleteConversationByConversationIDRequest): Objekt mit dem Feld conversation_id.

    Ablauf:
    - Ruft die Funktion `remove_conversation_by_conversation_id` auf, um die Konversation zu löschen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine passende Konversation gefunden oder gelöscht wurde.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigungsmeldung bei erfolgreichem Löschen.
    """
    conversation_id = request.conversation_id
    success = remove_conversation_by_conversation_id(conversation_id)

    if not success:
        raise HTTPException(status_code=404, detail="User or conversation not found or could not be deleted")

    print(f"Conversation '{conversation_id}' has been removed.")
    return {"message": f"Conversation '{conversation_id}' has been removed"}


class ConversationInputRequest(BaseModel):
    user_id: str

@app.post("/create_conversation")
async def create_chat_conversation(request: ConversationInputRequest):
    """
    Erstellt eine neue, leere Konversation für einen Benutzer.

    Parameter:
    - request (ConversationInputRequest): Objekt mit der user_id.

    Ablauf:
    - Generiert eine eindeutige conversation_id.
    - Initialisiert eine leere Konversation ohne Titel und ohne Dialogeinträge.
    - Speichert die Konversation mit `create_conversation`.
    - Gibt eine HTTP 409-Fehlermeldung zurück, wenn bereits eine Konversation mit der gleichen ID existiert.

    Rückgabewert:
    - JSON-Antwort mit Bestätigungsnachricht und generierter conversation_id.
    """
    user_id = request.user_id
    conversation_id = generate_conversation_id()
    print(conversation_id)
    title = ""
    dialog = []

    success = create_conversation(
        user_id=user_id,
        conversation_id=conversation_id,
        title=title,
        dialog=dialog
    )

    if not success:
        raise HTTPException(status_code=409, detail=f"Conversation with this conversation_id {conversation_id} already exists.")

    print("Conversation added successfully.")
    return {
        "message": "Conversation added successfully.",
        "conversation_id": conversation_id
    }


class DownloadConversationRequest(BaseModel):
    conversation_id: str

@app.post('/download_conversation')
async def download_conversation(request: DownloadConversationRequest):
    """
    Lädt ein Gespräch im PDF-Format herunter.

    Parameter:
    - request (DownloadConversationRequest): Objekt mit conversation_id.

    Ablauf:
    - Holt die Konversationsdaten über `get_conversations_dialogs`.
    - Erzeugt ein PDF über `Create_PDF`.
    - Gibt die PDF-Datei als Streaming-Antwort zurück.

    Rückgabewert:
    - StreamingResponse: PDF-Download als Stream.
    """
    conversation_id = request.conversation_id
    data = get_conversations_dialogs(conversation_id)
    
    if not data or 'conversations_dialogs' not in data:
        raise HTTPException(status_code=404, detail="No conversations dialogs found")

    conversations_dialogs = data.get('conversations_dialogs')
    pdf_data = Create_PDF.run_create_pdf(conversations_dialogs)

    pdf_buffer: BytesIO = pdf_data.get('pdf_buffer')
    filename: str = pdf_data.get('created_datetime_file_name')

    return StreamingResponse(
        pdf_buffer,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}.pdf"'}
    )


class SendConversationRequest(BaseModel):
    conversation_id: str
    email_address: str

@app.post('/send_conversation')
async def send_conversation(request: SendConversationRequest):
    """
    Sendet ein Gespräch per E-Mail als PDF-Anhang.

    Parameter:
    - request (SendConversationRequest): Objekt mit conversation_id und email_address.

    Ablauf:
    - Holt die Konversation.
    - Erstellt ein PDF.
    - Sendet das PDF an die angegebene E-Mail-Adresse.

    Rückgabewert:
    - JSON-Antwort mit Bestätigung.
    """
    conversation_id = request.conversation_id
    email_address = request.email_address
    data = get_conversations_dialogs(conversation_id)
    
    if not data or 'conversations_dialogs' not in data:
        raise HTTPException(status_code=404, detail="No conversations dialogs found")

    conversations_dialogs = data['conversations_dialogs']
    pdf_data = Create_PDF.run_create_pdf(conversations_dialogs)
    
    pdf_buffer = pdf_data.get('pdf_buffer')
    created_datetime_file_name = pdf_data.get('created_datetime_file_name')
    created_datetime_sending_time = pdf_data.get('created_datetime_sending_time')
    
    Send_Report_By_Email.run_send_report_by_mail(
        email_address,
        pdf_buffer,
        created_datetime_file_name,
        created_datetime_sending_time
    )
    
    return {"message": f"Report sent to {email_address} successfully"}


class DialogItemInputRequest(BaseModel):
    user_id: str
    conversation_id: str
    question: str
    answer: str
    date: str
    time: str

@app.post("/add_dialog_item")
async def post_add_dialog_item(request: DialogItemInputRequest):
    """
    Fügt einen einzelnen Frage-Antwort-Dialogeintrag zu einer bestehenden Konversation hinzu.

    Parameter:
    - request (DialogItemInputRequest): Benutzer-ID, Konversations-ID, Frage, Antwort, Datum und Uhrzeit.

    Rückgabewert:
    - JSON-Antwort bei Erfolg, 404-Fehler wenn Konversation nicht existiert.
    """
    success = add_dialog_item(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        question=request.question,
        answer=request.answer,
        date=request.date,
        time=request.time
    )

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found or could not be updated")

    return {"message": "Dialog item added successfully."}


class QAItem(BaseModel):
    question: str
    answer: str

class DialogTitleInputRequest(BaseModel):
    user_id: str
    conversation_id: str
    questions_and_answers: List[QAItem]

@app.post("/add_dialog_title")
async def post_add_dialog_title(request: DialogTitleInputRequest):
    """
    Generiert und speichert einen Titel basierend auf Fragen und Antworten für eine Konversation.

    Parameter:
    - request (DialogTitleInputRequest): Benutzer-ID, Konversations-ID und QA-Paare.

    Rückgabewert:
    - JSON-Antwort mit dem generierten Titel oder Fehler, wenn Konversation nicht existiert.
    """
    questions_and_answers = request.questions_and_answers
    title = create_conversation_title_gemini(questions_and_answers)
   
    success = add_dialog_title(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        title=title
    )

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    return {"message": title}


@app.post("/text_to_speech")
async def post_text_to_speech(text: str) -> StreamingResponse:
    """
    Wandelt Text in gesprochene Sprache um und gibt ihn als Stream zurück.

    Args:
        text (str): Der zu sprechende Text.

    Returns:
        StreamingResponse: Gestreamte Audiodatei.
    """
    answer_audio_bytes = run_text_to_speech(text)

    with open('audio.mp3', 'wb') as f:
        f.write(answer_audio_bytes)

    def get_audio():
        yield answer_audio_bytes

    return StreamingResponse(
        get_audio(),
        media_type="application/octet-stream"
    )


@app.post("/speech_to_text")
async def post_speech_to_text(speech: UploadFile = File(...)) -> dict:
    """
    Wandelt gesprochene Sprache in Text um.

    Args:
        speech (UploadFile): Hochgeladene Audiodatei.

    Returns:
        dict: Erkannter Text.
    """
    audio_bytes = await speech.read()
    text = run_speech_to_text(audio_bytes)
    return {"text": text}


@app.post("/conversations_dialogs/{conversation_id}")
async def post_conversations_dialogs(conversation_id: str):
    """
    Gibt die Dialogeinträge einer Konversation formatiert für das Frontend zurück.

    Parameter:
    - conversation_id (str): Die ID der Konversation.

    Rückgabewert:
    - JSON-Antwort mit formatierten Dialogeinträgen oder 404-Fehlermeldung.
    """
    data = get_conversations_dialogs(conversation_id)

    if not data or 'conversations_dialogs' not in data or not data['conversations_dialogs']:
        raise HTTPException(status_code=404, detail="No conversation dialogs found")

    formatted_dialogs = []
    for dialog in data['conversations_dialogs']:
        formatted_dialogs.append({
            'question': dialog.get('question', ''),
            'answer': dialog.get('answer', ''),
            'date': dialog.get('date', ''),
            'time': dialog.get('time', '')
        })

    return {'conversations_dialogs': formatted_dialogs}
