import time
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from src.database import get_vectorstore
from src.logger import registrar_tool_trace 

vectorstore = get_vectorstore()

@tool
def buscar_en_documentos(pregunta: str) -> str:
    """Úsala para buscar información sobre reglamentos, útiles, lecturas o profesores."""
    inicio_tiempo_tool = time.time() # Iniciamos cronómetro de la tool
    
    if not vectorstore:
        resultado = "Error interno: No hay conexión a la base de datos."
    else:
        docs = vectorstore.similarity_search(pregunta, k=3)
        resultado = "\n\n".join(doc.page_content for doc in docs)
        
        if len(resultado) == 0:
            resultado = "No se encontró información en la base de datos."
            
    latencia_tool = time.time() - inicio_tiempo_tool # Paramos cronómetro
    
    # 🚀 Registramos el "entre medio"
    registrar_tool_trace("buscar_en_documentos", {"pregunta": pregunta}, resultado, latencia_tool)
    
    return resultado

@tool
def consultar_web_colegio() -> str:
    """Úsala para buscar teléfonos, correos electrónicos, dirección o contacto."""
    inicio_tiempo_tool = time.time() # Iniciamos cronómetro de la tool
    url = "https://www.redwoodcollege.cl/" 
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        texto_limpio = soup.get_text(separator=' ', strip=True)
        
        if len(texto_limpio) < 50:
            resultado = "Error: Pude entrar a la web, pero el texto está oculto."
        else:
            resultado = f"Información de la web: {texto_limpio[:3000]}"
            
    except Exception as e:
        resultado = f"No se pudo acceder a la página web. Error: {e}"
        
    latencia_tool = time.time() - inicio_tiempo_tool # ⏱️ Paramos cronómetro
    
    # Registramos el "entre medio"
    registrar_tool_trace("consultar_web_colegio", {}, resultado, latencia_tool)
    
    return resultado