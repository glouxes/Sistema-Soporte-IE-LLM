import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No se encontró GOOGLE_API_KEY en el .env")
else:
    try:
        genai.configure(api_key=api_key)
        print("--- Modelos Disponibles para tu API Key ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" {m.name}")
    except Exception as e:
        print(f"Error de conexión o API Key: {e}")