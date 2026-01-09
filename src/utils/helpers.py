import logging
import os

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("data/outputs/sistema_extraccion.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("SistemaSoporte")

def save_json(data, filename):
    import json
    path = os.path.join("data/outputs", filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return path