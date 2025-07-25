# Diese Methode konvertiert einen Text mittles AI in Audio
# Die Doku steht in https://api.voicerss.org/
# Fehler (Exceptions) wurden mit ChatGPT erstellt
def run_text_to_speech(text):
    import requests
    from decouple import config

   
    API_KEY = config("VOICERSS_API_KEY")

    params = {
        'key': API_KEY,
        'hl': 'de-de',
        'src': text,
        'c': 'MP3',
        'f': '44khz_16bit_stereo'
    }

    response = requests.get('https://api.voicerss.org/', params=params)

    return response.content

