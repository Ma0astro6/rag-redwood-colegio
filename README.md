# 🌲 RAG Asistente Redwood College

Un chatbot con arquitectura RAG (Retrieval-Augmented Generation) desarrollado para responder preguntas basadas en el reglamento oficial del colegio. 

## 🛠️ Arquitectura y Tecnologías
Este proyecto fue adaptado para ejecutarse de forma **100% local y gratuita**, utilizando las siguientes herramientas:

* **UI:** Streamlit
* **Orquestador:** LangChain (LCEL)
* **LLM:** `llama-3.1-8b-instant` (Vía Groq API)
* **Embeddings:** `all-MiniLM-L6-v2` (Vía HuggingFace - Local)
* **Base de Datos Vectorial:** FAISS (Local)
* **Procesamiento de Documentos:** PyPDF2

## 🚀 Cómo iniciar la aplicación (Setup)

Sigue estos pasos para levantar el proyecto en tu máquina local:

### 1. Clonar el repositorio
Descarga este proyecto en tu computador e ingresa a la carpeta:
```bash
git clone <URL-DE-TU-REPOSITORIO>
cd PWOOD

### 2. Crear y activar el Entorno Virtual
Para evitar conflictos con otras librerías, crea una "burbuja" de Python (en Windows):

py -m venv venv
.\venv\Scripts\activate

### 3. Instalar dependencias
Con el entorno activado, instala todas las librerías necesarias:

pip install -r requirements.txt

### 4. Ejecutar la aplicación

streamlit run app.py