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
            self.logger.error("No se encontró la GOOGLE_API_KEY en el entorno.")
            raise ValueError("Falta GOOGLE_API_KEY en el archivo .env")
        
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(model_name='models/gemini-flash-latest')
        
        try:
            with open(golden_set_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        except Exception as e:
            self.logger.error(f"Error al cargar el esquema JSON: {e}")
            raise

    def transform(self, raw_text, metadata):
        prompt = self._prepare_prompt(raw_text)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1  
                }
            )
            
            if not response or not response.text:
                raise Exception("El modelo no devolvió contenido.")

            extracted_data = json.loads(response.text)
            
            extracted_data["metadata_documento"] = metadata
            
            validate(instance=extracted_data, schema=self.schema)
            
            self.logger.info("Transformación y validación exitosa.")
            return extracted_data

        except ValidationError as ve:
            self.logger.error(f"Error de cumplimiento de esquema: {ve.message}")
            return {
                "error": "El modelo falló en la estructura fáctica", 
                "details": ve.message,
                "raw_output": response.text if 'response' in locals() else None
            }
        except Exception as e:
            self.logger.error(f"Error crítico en la llamada a Gemini: {e}")
            return {"error": "Fallo en la conexión con el LLM", "mensaje": str(e)}

    def _prepare_prompt(self, text):
        """
        Crea el prompt de ingeniería para el modelo.
        """
        campos_esperados = json.dumps(self.schema.get('properties', self.schema.get('propiedades', {})), indent=2)
        
        return f"""
            Actúa como un motor ETL (Extract, Transform, Load) especializado en documentos oficiales mexicanos.
            Tu objetivo es realizar una extracción fáctica del TEXTO proporcionado y mapearlo exactamente al esquema JSON.

            REGLAS CRÍTICAS:
            1. No inventes datos. Si un campo no es visible en el texto, escribe null.
            2. No incluyas explicaciones ni formato Markdown (como ```json), entrega solo el objeto JSON puro.
            3. Formatea las fechas a YYYY-MM-DD si es posible.
            4. Los campos que debes extraer son:
            {campos_esperados}

            TEXTO A PROCESAR:
            {text}
            """