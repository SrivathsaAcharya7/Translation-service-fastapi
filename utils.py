import openai
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv
import os
import requests
load_dotenv()

LIBRETRANSLATE_URL = "http://localhost:5000/translate"

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}

    for lang in languages:
        try:
            # Print the input to debug the text being sent
            print(f"Translating to {lang}: {text}")
            # Send POST request to LibreTranslate API with JSON payload and headers
            response = requests.post(LIBRETRANSLATE_URL, json={
                'q': text,
                'source': 'en',
                'target': lang,
                'format': 'text'
            }, headers={'Content-Type': 'application/json'})
            # Print the full response to debug
            print(f"Response from LibreTranslate (HTTP {response.status_code}): {response.text}")
            # Check if the request was successful
            if response.status_code == 200:
                translated_text = response.json().get('translatedText')
                print(translated_text)
                if translated_text:
                    translations[lang] = translated_text
                    print(translations)
                else:
                    translations[lang] = "Translation not found in response"
            else:
                translations[lang] = f"Error: HTTP {response.status_code}"
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error: {e}"
    # Update the translation task in the database with the translations
    update_translation_task(db, task_id, translations)
