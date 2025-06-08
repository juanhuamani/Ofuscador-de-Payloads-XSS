import pandas as pd
from transformers import pipeline
import torch
from tqdm import tqdm
import time

# 1. Configuración del modelo
print("⚡ Configurando ofuscador ultra-rápido...")
device = 0 if torch.cuda.is_available() else -1
obfuscator = pipeline(
    "text2text-generation",
    model="t5-small",
    device=device,
    framework="pt",
    truncation=True
)

# 2. Cargar dataset
print("📂 Cargando dataset...")
df = pd.read_csv('xss_balanced_dataset.csv')
malicious_samples = df[df['label'] == 1]['payload'].tolist()
print(f"🔢 Total payloads a ofuscar: {len(malicious_samples)}")

# 3. Ofuscar uno a uno con barra de progreso
def ofuscar_payload(payload):
    try:
        resultado = obfuscator(
            f"Obfuscate this XSS: {payload}",
            max_new_tokens=128,
            num_beams=1,
            temperature=0.8,
            do_sample=True
        )
        return resultado[0]['generated_text']
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return ""

# 4. Ejecutar y medir tiempo
print("\n🚀 Iniciando proceso de ofuscación...")
ofuscados = []
start_time = time.time()

for payload in tqdm(malicious_samples, desc="🚀 Ofuscando payloads"):
    ofuscado = ofuscar_payload(payload)
    ofuscados.append(ofuscado)

total_time = time.time() - start_time

# 5. Guardar resultados
output_df = pd.DataFrame({
    'original': malicious_samples,
    'ofuscado': ofuscados
})
output_filename = 'payloads_ofuscados_con_progreso.csv'
output_df.to_csv(output_filename, index=False)

# 6. Resumen
print(f"\n✅ ¡Completado! {len(ofuscados)} payloads procesados")
print(f"⏱️ Tiempo total: {total_time:.2f} segundos")
print(f"⚡ Velocidad: {len(ofuscados)/total_time:.1f} payloads/segundo")
print(f"💾 Resultados guardados en '{output_filename}'")
