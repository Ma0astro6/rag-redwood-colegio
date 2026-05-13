# 🌲 Agente Inteligente Redwood College (RAG + Web Scraper)

Un agente virtual autónomo con arquitectura basada en grafos (LangGraph) desarrollado para automatizar la atención de consultas del colegio. El agente toma decisiones adaptativas, recupera información del reglamento oficial (RAG) y extrae datos dinámicos en tiempo real desde la web oficial.

## 🛠️ Arquitectura y Tecnologías
Este proyecto fue adaptado para ejecutarse de forma **100% local y gratuita** en el procesamiento de datos, utilizando las siguientes herramientas:

* **Frontend y Memoria Visual:** Streamlit
* **Orquestador de Agentes:** LangGraph (ReAct Agent)
* **LLM (Cerebro):** `llama-3.1-8b-instant` (Vía Groq API)
* **Embeddings:** `all-MiniLM-L6-v2` (Vía HuggingFace - Local)
* **Base de Datos Vectorial:** FAISS (Local)
* **Navegación Autónoma (Web Scraping):** Requests + BeautifulSoup4
* **Procesamiento de Documentos:** PyPDF2

## 📂 Estructura del Proyecto

El proyecto separa la capa de presentación de la lógica de negocio:

```text
/
├── public/                 # Archivos estáticos
│   └── reglamento.pdf      # Documento base para el RAG
├── src/                    # Lógica del Backend
│   ├── agent.py            # Configuración del grafo (LLM) y System Prompt
│   └── tools.py            # Herramientas del agente (FAISS Retriever y Web Scraper)
├── app.py                  # Interfaz gráfica y gestión de memoria cognitiva
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación


🚀 Cómo iniciar la aplicación (Setup)

Sigue estos pasos para levantar el proyecto en tu máquina local:
1. Clonar el repositorio

Descarga este proyecto en tu computador e ingresa a la carpeta:
Bash

git clone <URL-DE-TU-REPOSITORIO>
cd PWOOD

2. Crear y activar el Entorno Virtual

Para evitar conflictos con otras librerías, crea una "burbuja" de Python (comandos para Windows):
Bash

py -m venv venv
.\venv\Scripts\activate

3. Instalar dependencias

Con el entorno activado, instala todas las librerías necesarias (asegurando compatibilidad de versiones):
Bash

pip install -r requirements.txt

4. Ejecutar la aplicación

Levanta el servidor local de Streamlit:
Bash

streamlit run app.py

Nota: Al abrir la interfaz web, ingresa tu API Key de Groq en la barra lateral para despertar al agente y cargar las herramientas en memoria.

