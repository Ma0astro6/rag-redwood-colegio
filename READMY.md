# Asistente Virtual RAG - Colegio Redwood

## Descripción
Este proyecto es un asistente virtual desarrollado para el Colegio Redwood. Utiliza Streamlit para la interfaz y prepara la arquitectura para un pipeline RAG (Retrieval-Augmented Generation) con LangChain.

## Instrucciones para ejecutar el proyecto (Docker)
Para que el evaluador pueda levantar este sistema sin problemas de dependencias, siga estos pasos:

1. Clone este repositorio en su máquina local.
2. Abra una terminal en la carpeta del proyecto.
3. Construya la imagen de Docker con el comando:
   `docker build -t redwood-bot .`
4. Ejecute el contenedor con el comando:
   `docker run -p 8501:8501 redwood-bot`
5. Abra su navegador web e ingrese a `http://localhost:8501`