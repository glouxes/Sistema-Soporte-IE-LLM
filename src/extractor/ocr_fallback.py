import pytesseract
from pdf2image import convert_from_path

class OCRFallback:
    def __init__(self, tesseract_path=r'D:\Tesseract-OCR\tesseract.exe', poppler_path=r"D:\poppler-25.07.0\bin"):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.poppler_path = poppler_path

    def extract_text(self, pdf_path):
        images = convert_from_path(pdf_path, poppler_path=self.poppler_path)
        full_text = ""
        for img in images:
            full_text += pytesseract.image_to_string(img, lang='spa')
        return full_text