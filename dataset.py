import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# 1.1. Maliciosos: Kaggle
try:
    kaggle_xss = pd.read_csv('XSS_dataset.csv')
    print("Dataset de Kaggle cargado exitosamente")
except FileNotFoundError:
    print("Archivo xss_dataset_kaggle.csv no encontrado. Por favor, descárgalo de: https://www.kaggle.com/datasets/syedsaqlainhussain/xss-dataset-for-deep-learning")
    kaggle_xss = pd.DataFrame(columns=['payload', 'label'])

# 1.2. Maliciosos: PortSwigger Cheat Sheet
def get_portswigger_payloads():
    print("Obteniendo payloads de PortSwigger...")
    url = "https://portswigger.net/web-security/cross-site-scripting/cheat-sheet"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    payloads = [code.text for code in soup.select('code')]
    print(f"Se encontraron {len(payloads)} payloads en PortSwigger")
    return payloads

# 1.3. Benignos: Bootstrap y Materialize JS
def extract_js_code(directory):
    print(f"Extrayendo código JS de {directory}...")
    js_code = []
    if not os.path.exists(directory):
        print(f"Directorio {directory} no encontrado")
        return js_code
        
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                try:
                    with open(os.path.join(root, file), 'r', errors='ignore') as f:
                        js_code.append(f.read())
                except Exception as e:
                    print(f"Error al leer {file}: {str(e)}")
    print(f"Se extrajeron {len(js_code)} archivos JS de {directory}")
    return js_code

# Ejecutar las funciones
print("\nIniciando recolección de datos...")

# Obtener payloads de PortSwigger
portswigger_payloads = get_portswigger_payloads()

# Extraer código JS
bootstrap_js = extract_js_code('bootstrap/')
materialize_js = extract_js_code('materialize/')

print("\nResumen:")
print(f"- Payloads de Kaggle: {len(kaggle_xss)}")
print(f"- Payloads de PortSwigger: {len(portswigger_payloads)}")
print(f"- Archivos JS de Bootstrap: {len(bootstrap_js)}")
print(f"- Archivos JS de Materialize: {len(materialize_js)}")