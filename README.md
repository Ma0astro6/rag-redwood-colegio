# 🌲 Agente Inteligente Redwood College (RAG + Web Scraper + Observabilidad)

Un agente virtual autónomo con arquitectura basada en grafos (LangGraph) desarrollado para automatizar la atención de consultas del colegio. Este proyecto incluye un sistema RAG en la nube, extracción de datos dinámicos mediante Web Scraping y un **módulo completo de observabilidad y trazabilidad** para monitorear latencia, tokens y seguridad en tiempo real.

## 🛠️ Arquitectura y Tecnologías
Este proyecto fue refactorizado siguiendo los principios de **Arquitectura Limpia (SOLID)** y utiliza herramientas de vanguardia:

* **Frontend y Dashboard:** Streamlit + Pandas
* **Orquestador de Agentes:** LangGraph (StateGraph construido manualmente con manejo de nodos y edges)
* **LLM (Cerebro):** `llama-3.3-70b-versatile` (Vía Groq API)
* **Embeddings:** `all-MiniLM-L6-v2` (Vía HuggingFace - Local)
* **Base de Datos Vectorial:** MongoDB Atlas (Cloud Vector Search con índice estructurado)
* **Navegación Autónoma:** Requests + BeautifulSoup4
* **Trazabilidad y Observabilidad:** Sistema de logging JSON nativo para capturar RTT (latencia) y uso de memoria cognitiva.

## 📂 Estructura del Proyecto

El proyecto separa estrictamente la capa de presentación, la lógica del negocio y las bases de datos:

```text
/
├── app.py                  # Interfaz gráfica principal (Chatbot)
├── agent_logs.json         # (Autogenerado) Archivo de trazabilidad y métricas
├── pages/
│   └── 1_📊_Dashboard.py   # Panel visual interactivo de métricas y KPIs
├── src/                    # Lógica del Backend
│   ├── agent.py            # Construcción del StateGraph y orquestación
│   ├── database.py         # Conexión aislada a MongoDB Atlas
│   ├── logger.py           # Motor de intercepción de métricas (Latencia, Tokens, Errores)
│   ├── prompts.py          # System Prompt estructurado con Guardrails éticos
│   └── tools.py            # Herramientas del agente (Vector Retriever y Web Scraper)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación

🚀 Guía de Ejecución para Evaluadores (Setup)

Sigue estos pasos para levantar el proyecto y validar su funcionamiento y observabilidad en tu máquina local:
1. Clonar el repositorio

Descarga este proyecto en tu computador e ingresa a la carpeta raíz:
Bash

git clone <URL-DE-TU-REPOSITORIO>
cd PWOOD

2. Crear y activar el Entorno Virtual

Para evitar conflictos con otras librerías, crea un entorno virtual (comandos para Windows):
Bash

py -m venv venv
.\venv\Scripts\activate

3. Instalar dependencias

Con el entorno activado, instala todas las librerías necesarias:
Bash

pip install -r requirements.txt

4. Ejecutar la aplicación

Levanta el servidor multipágina de Streamlit:
Bash

streamlit run app.py