# SSD-IE: Sistema de Soporte para Extracción de Información con Modelos de Lenguaje Largo

Este proyecto es un motor inteligente de **Extracción, Transformación y Carga (ETL)** diseñado para automatizar la captura de datos de documentos oficiales (como la INE, CURP, NSS, etc.). Utiliza una arquitectura híbrida que combina extracción nativa de PDFs, OCR (Reconocimiento Óptico de Caracteres) y el modelo de lenguaje **Gemini 1.5 Flash**.

### Etapas del proceso:
- **Estrategia Híbrida de Ingesta:** Prioriza la extracción rápida con PyMuPDF y activa automáticamente Tesseract OCR para documentos escaneados.
- **Transformación Semántica:** Limpieza y estructuración de texto mediante IA.
- **Validación Fáctica:** Garantiza que la salida cumpla con el esquema definido en el **Golden Set**.
- **Pipeline de Decisión:** Evalúa la calidad del texto antes de decidir el siguiente paso en el flujo.

##  Estructura del Proyecto

El repositorio está organizado siguiendo principios de modularidad:

├── data/
│   ├── inputs/          # Documentos PDF a procesar (INE, CURP, etc.)
│   └── schema/          # Definición del Golden Set (golden_set.json)
├── src/
│   ├── extractor/       # Motores de extracción (pdf_engine.py, ocr_fallback.py)
│   ├── transformer/     # Lógica de la IA (agent.py)
│   └── utils/           # Ayudantes para logs y guardado de archivos
├── main.py              # Punto de entrada principal del sistema
├── check_models.py      # Script de verificación de conexión con Google AI
├── requirements.txt     # Dependencias del proyecto
└── .env                 # Variables de entorno (API Keys)

## Requisitos de instalación

Este proyecto requiere tener instalados en el sistema:

 **Tesseract OCR** 
Link de descarga: https://github.com/UB-Mannheim/tesseract/wiki
Deberá descargar el archivo llamado tesseract-ocr-w64-setup-5.x.x.exe
Nota: Durante la instalación, busque la sección de "Additional script data" y "Additional language data" y marque la casilla de Spanish (Español) para que reconozca tildes y la "ñ".

** Poppler (para conversión de PDF a imagen)**
Poppler no tiene un instalador tradicional, se descarga como una carpeta de archivos binarios que se deben descomprimir.
Link de descarga: [Poppler for Windows (vía @oschwartz10612)](https://github.com/oschwartz10612/poppler-windows/releases/)
Deberá descargar el archivo .zip de la versión más reciente (ej. Release-24.08.0-0.zip).
Descomprímalo en una ruta sencilla, por ejemplo: D:\poppler.

Una vez instados en el equipo, se deberán copiar las rutas tanto del archivo tesseract.exe y la carpeta bin de poppler y modificarlas segun sea el caso en el script ocr_fallback.py. 
En el proyecto se decidieron guardar en el disco D:
tesseract_path=r'D:\Tesseract-OCR\tesseract.exe', poppler_path=r"D:\poppler-25.07.0\bin"


## Variables de entorno

Dado que se trabaja con un modelo de lenguaje es necesario trabajar con una llave de acceso, esta se puede descargar en el link https://aistudio.google.com/app/api-keys. 
Una vez creada la llave se deberá crear una carpeta llamada "venv" en la raiz del proyecto.
Cree un nuevo archivo en la raiz del proyecto  nombrándolo ".env", copie el siguiente contenido agregando la api key previamente creada:

GOOGLE_API_KEY="Su_API_Key_sin_comillas"
ENV=development
LOG_LEVEL=INFO



# Prueba del sistema
Para poner en marcha el proyecto una vez instalando y agregando las variables de entorno mencionadas en el punto anterior siga los pasos.
Abra una terminal y pegue los siguientes comandos: 

## 1. Clonar el repositorio:

git clone https://github.com/glouxes/Sistema-Soporte-IE-LLM.git
cd SSD-IE

## 2. Configurar el entorno virtual

Configure el entorno con lo siguiente:

python -m venv venv
source venv/Scripts/activate  # para Windows
pip install -r requirements.txt

## Pruebas
Una vez todo listo el funcionamiento del sistema es muy sencillo. En el script de python main.py modifique la ruta del documento al cual se quiera realizar la extracción y su tipo de fuente. Usted podrá encontrar en la carpeta "inputs" los archivos que quiera probar, se pueden agregar más si se desea probar con otros documentos diferentes.

Ejecute 
python main.py 