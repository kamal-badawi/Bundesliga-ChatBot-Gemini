# Diese Methode konvertiert einen Audio mittles AI in Text 
# Die Doku steht in https://api.assemblyai.com
# Fehler (Exceptions) wurden mit ChatGPT erstellt

def run_speech_to_text(audio_file):
    import requests
    import time
    from decouple import config
    

    base_url = "https://api.assemblyai.com"
    

    API_KEY = config("ASSEMBLYAI_API_KEY")
    if not API_KEY:
        raise ValueError("API-Key konnte nicht geladen werden. Bitte prüfe deine .env-Datei.")

    headers = {
        'authorization': API_KEY,
        'content-type': 'application/octet-stream'
    }

    
    response = requests.post(f"{base_url}/v2/upload", headers=headers, data=audio_file)
    if response.status_code != 200:
        raise RuntimeError(f"Fehler beim Hochladen: {response.status_code}")

    audio_url = response.json()["upload_url"]

    
    transcript_request = {
        "audio_url": audio_url,
        "language_code": "de",
        "speech_model": "universal"
    }

    transcript_response = requests.post(
        f"{base_url}/v2/transcript",
        json=transcript_request,
        headers={'authorization': API_KEY}
    )

    if transcript_response.status_code != 200:
        raise RuntimeError("Transkriptionsanforderung fehlgeschlagen.")

    transcript_id = transcript_response.json()["id"]
    polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

    
    while True:
        polling_response = requests.get(polling_endpoint, headers={'authorization': API_KEY})
        result = polling_response.json()

        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            raise RuntimeError(f"Transkription fehlgeschlagen: {result['error']}")
        else:
            time.sleep(3)
