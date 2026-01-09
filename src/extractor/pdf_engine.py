import fitz
import logging

class PDFEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_content(self, pdf_path):
        text_results = []
        try:
            doc = fitz.open(pdf_path)
            for page_num, page in enumerate(doc):
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                page_text = "\n".join([b[4] for b in blocks if b[4].strip()])
                text_results.append(page_text)
            
            full_text = "\n--- Nueva Página ---\n".join(text_results)
            
            if len(full_text.strip()) < 100:
                self.logger.warning(f"Calidad baja detectada en {pdf_path}. Pocos caracteres extraídos.")
                return full_text, False 
                
            return full_text, True
        except Exception as e:
            self.logger.error(f"Error crítico en PyMuPDF: {e}")
            return "", False