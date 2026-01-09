import time
import hashlib
from datetime import datetime
from src.extractor.pdf_engine import PDFEngine
from src.extractor.ocr_fallback import OCRFallback 
from src.transformer.agent import ETLAgent
from src.utils.helpers import setup_logger, save_json

def main(archivo_entrada, tipo_fuente="OTRO"):
    logger = setup_logger()
    start_time = time.time()
    
    file_id = hashlib.md5(archivo_entrada.encode()).hexdigest()
    metadata = {
        "identificador_documento": file_id,
        "fecha_extraccion": datetime.now().isoformat(),
        "fuente_original": tipo_fuente
    }

    pdf_tool = PDFEngine()
    texto_crudo, es_calidad_alta = pdf_tool.extract_content(archivo_entrada)

    if not es_calidad_alta:
        logger.warning(f"Calidad baja en {archivo_entrada}. Iniciando OCR Fallback...")
        ocr_tool = OCRFallback()
        texto_crudo = ocr_tool.extract_text(archivo_entrada)

    try:
        agente = ETLAgent("data/schema/golden_set.json")
        resultado = agente.transform(texto_crudo, metadata)
        
        latencia = time.time() - start_time
        logger.info(f"Proceso completo en {latencia:.2f}s para {archivo_entrada}")
        
        save_json(resultado, f"resultado_{file_id}.json")
        print(f"Extracción exitosa: resultado_{file_id}.json")
        
    except Exception as e:
        logger.error(f"Error crítico en el pipeline: {e}")

if __name__ == "__main__":
    main("data/inputs/mi_ine.pdf", tipo_fuente="INE")