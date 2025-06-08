import pandas as pd
import os
import re
from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np

# Configuración
np.random.seed(42)

# 1. Extracción de fragmentos JS
def extract_js_fragments(directory, max_samples=7000):
    fragments = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                try:
                    with open(Path(root)/file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        chunks = re.split(r'(function\s+\w+|class\s+\w+)', content)
                        fragments.extend([chunk.strip() for chunk in chunks if 50 < len(chunk) < 2000])
                except Exception as e:
                    print(f"Error en {file}: {str(e)}")
    return list(set(fragments))[:max_samples]

# 2. Scraping completo de PortSwigger
def get_full_portswigger_payloads():
    print("Obteniendo payloads de PortSwigger con Selenium...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://portswigger.net/web-security/cross-site-scripting/cheat-sheet")
        driver.implicitly_wait(10)
        
        # Expandir todas las secciones
        expand_buttons = driver.find_elements("css selector", "button.bp3-button")
        for btn in expand_buttons:
            if 'Expand' in btn.get_attribute('innerHTML'):
                driver.execute_script("arguments[0].click();", btn)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        payloads = list(set([code.get_text(strip=True) for code in soup.find_all('code')]))
        return payloads
    finally:
        driver.quit()

# 3. Cargar y procesar Kaggle
print("Cargando dataset de Kaggle...")
kaggle_data = pd.read_csv('XSS_dataset.csv')
benign_kaggle = kaggle_data[kaggle_data['Label'] == 0]['Sentence'].tolist()
malicious_kaggle = kaggle_data[kaggle_data['Label'] == 1]['Sentence'].tolist()

# 4. Extraer código de repositorios
print("Extrayendo código JS de bootstrap...")
bootstrap_js = extract_js_fragments('bootstrap', 6000)
print(f"Fragmentos de Bootstrap: {len(bootstrap_js)}")

print("Extrayendo código JS de materialize...")
materialize_js = extract_js_fragments('materialize', 4000)
print(f"Fragmentos de Materialize: {len(materialize_js)}")

# 5. Obtener payloads de PortSwigger
portswigger_payloads = get_full_portswigger_payloads()
print(f"Payloads de PortSwigger: {len(portswigger_payloads)}")

# 6. Construir DataFrames balanceados
df_benign = pd.DataFrame({
    'payload': benign_kaggle[:6000] + bootstrap_js[:4000] + materialize_js[:2038],
    'label': 0
})[:12038]  # Total 12,038

df_malicious = pd.DataFrame({
    'payload': malicious_kaggle[:6000] + portswigger_payloads[:1321],
    'label': 1
})[:7321]  # Total 7,321

# 7. Combinar y limpiar
df = pd.concat([df_benign, df_malicious])
df['payload'] = df['payload'].str.lower().str.replace(r'\s+', ' ', regex=True)
df.drop_duplicates(subset=['payload'], inplace=True)

# 8. Verificar balanceo
print("\nDistribución final:")
print(f"Total muestras: {len(df)}")
print(f"Benignos: {len(df[df['label']==0])} ({len(df[df['label']==0])/len(df)*100:.1f}%)")
print(f"Maliciosos: {len(df[df['label']==1])} ({len(df[df['label']==1])/len(df)*100:.1f}%)")

# Guardar
df.to_csv('xss_balanced_dataset.csv', index=False)
print("Dataset guardado correctamente")