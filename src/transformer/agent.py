import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from jsonschema import validate, ValidationError

load_dotenv()

class ETLAgent:
    def __init__(self, golden_set_path):
        self.logger = logging.getLogger(__name__)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Falta GOOGLE_API_KEY en el archivo .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        with open(golden_set_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)

    def transform(self, raw_text, metadata):
        prompt = self._prepare_prompt(raw_text)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json"
                }
            )
            
            extracted_data = json.loads(response.text)
            
            extracted_data["metadata_documento"] = metadata
            
            validate(instance=extracted_data, schema=self.schema)
            
            return extracted_data

        except ValidationError as ve:
            self.logger.error(f"Error de validación: {ve.message}")
            return {"error": "El modelo falló en la estructura fáctica", "details": ve.message}
        except Exception as e:
            self.logger.error(f"Error en la llamada a Gemini: {e}")
            return {"error": "Fallo en la conexión con el LLM"}

    def _prepare_prompt(self, text):
        return f"""
        Actúa como un motor ETL de extracción fáctica. 
        Tu objetivo es convertir el TEXTO proporcionado al esquema JSON definido.
        
        REGLAS:
        1. No incluyas explicaciones, solo el JSON.
        2. Si un dato no está presente, escribe null.
        3. Extrae exactamente según estos campos:
        {json.dumps(self.schema['propiedades'], indent=2)}
        
        TEXTO:
        {text}
        """