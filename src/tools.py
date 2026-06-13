import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from src.database import get_vectorstore 

# Obtenemos la instancia de la base de datos
vectorstore = get_vectorstore()

@tool
def buscar_en_documentos(pregunta: str) -> str:
    """Úsala para buscar información sobre reglamentos, útiles, lecturas o profesores."""
    print(f"🚨 EL AGENTE ESTÁ BUSCANDO EN MONGO: {pregunta}") 
    
    if not vectorstore:
        return "Error interno: No hay conexión a la base de datos."
        
    docs = vectorstore.similarity_search(pregunta, k=3)
    contexto_encontrado = "\n\n".join(doc.page_content for doc in docs)
    
    print(f"📦 MONGO DEVOLVIÓ {len(docs)} DOCUMENTOS CON {len(contexto_encontrado)} CARACTERES.")
    
    if len(contexto_encontrado) == 0:
        return "No se encontró información en la base de datos."
    return contexto_encontrado

@tool
def consultar_web_colegio() -> str:
    """Úsala para buscar teléfonos, correos electrónicos, dirección o contacto."""
    print("🚨 EL AGENTE ESTÁ LEYENDO LA PÁGINA WEB OFICIAL") 
    
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
        
        print(f"🌐 LA WEB DEVOLVIÓ {len(texto_limpio)} CARACTERES.") 
        
        if len(texto_limpio) < 50:
            return "Error: Pude entrar a la web, pero el texto está oculto."
            
        return f"Información de la web: {texto_limpio[:3000]}"
    except Exception as e:
        error_msg = f"No se pudo acceder a la página web. Error: {e}"
        print(f"❌ ERROR WEB: {error_msg}")
        return error_msg