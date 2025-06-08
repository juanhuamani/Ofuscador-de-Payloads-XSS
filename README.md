# Ofuscador de Payloads XSS

![XSS Obfuscation](https://raw.githubusercontent.com/yourusername/xss-obfuscator/main/docs/xss-obfuscation.png)

## 🎯 Propósito

Este proyecto implementa un sistema de ofuscación de payloads XSS utilizando modelos de lenguaje avanzados. El objetivo es generar variantes ofuscadas de payloads XSS conocidos para mejorar la detección y prevención de ataques.

## 🚀 Características

- Ofuscación automática de payloads XSS
- Procesamiento en paralelo para mayor velocidad
- Utiliza el modelo T5 de Hugging Face
- Soporte para GPU (CUDA)
- Generación de variantes múltiples

## 📋 Requisitos

```bash
pip install torch transformers pandas sentencepiece
```

## 💻 Uso

1. Prepara tu dataset en formato CSV con las columnas:
   - `payload`: El payload XSS original
   - `label`: Etiqueta (1 para malicioso, 0 para benigno)

2. Ejecuta el script:
```bash
python obfuscador.py
```

3. Los resultados se guardarán en `payloads_ofuscados_express.csv`

## 🔧 Configuración

El script puede ser configurado modificando los siguientes parámetros:

- `batch_size`: Tamaño del lote para procesamiento
- `max_new_tokens`: Longitud máxima de la salida generada
- `temperature`: Controla la aleatoriedad de la generación
- `num_beams`: Número de beams para la búsqueda

## 📊 Ejemplo de Resultados

```
Payload Original: <script>alert(1)</script>
Payload Ofuscado: <scr\x00ipt>al\u0065rt(1)</scr\x00ipt>
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 