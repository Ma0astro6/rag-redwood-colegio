import os
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import docx
import requests
from bs4 import BeautifulSoup

# 1. Ruta estática
carpeta_public = "public"
vectorstore = None

# 2. Pre-cargar la base de datos vectorial en memoria (Escalabilidad Total)
try:
    texto_completo = ""
    archivos_leidos = 0

    if os.path.exists(carpeta_public):
        for nombre_archivo in os.listdir(carpeta_public):
            ruta_archivo = os.path.join(carpeta_public, nombre_archivo)
            
            # Si es un PDF, lo lee así:
            if nombre_archivo.endswith(".pdf"):
                with open(ruta_archivo, "rb") as archivo:
                    lector = PyPDF2.PdfReader(archivo)
                    for pagina in lector.pages:
                        texto_completo += pagina.extract_text() or ""
                archivos_leidos += 1
                print(f"📄 Cargando PDF: {nombre_archivo}")
            
            # Si es un Word, lo lee así:
            elif nombre_archivo.endswith(".docx"):
                # Omitir archivos temporales que crea Windows (los que empiezan con ~$)
                if not nombre_archivo.startswith("~$"):
                    doc = docx.Document(ruta_archivo)
                    for parrafo in doc.paragraphs:
                        texto_completo += parrafo.text + "\n"
                    archivos_leidos += 1
                    print(f"📝 Cargando Word: {nombre_archivo}")

        # Vectorizar todo el conocimiento junto
        if archivos_leidos > 0:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            chunks = text_splitter.split_text(texto_completo)
            
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_texts(chunks, embeddings)
            print(f"✅ ¡Cerebro cargado! {archivos_leidos} documentos indexados correctamente.")
        else:
            print("⚠️ No se encontraron documentos válidos en la carpeta.")
    else:
        print(f"❌ Error: No existe la carpeta {carpeta_public}")
except Exception as e:
    print(f"Error procesando los documentos: {e}")

# 3. LA HERRAMIENTA DEL AGENTE
@tool
def buscar_en_documentos(pregunta: str) -> str:
    """
    Utiliza esta herramienta SIEMPRE para buscar información sobre el reglamento, 
    listas de útiles, lecturas complementarias o profesores.
    """
    if vectorstore is None:
        return "Error: La base de datos de documentos no está disponible."
    
    docs = vectorstore.similarity_search(pregunta, k=6) 
    contexto_encontrado = "\n\n".join(doc.page_content for doc in docs)
    return contexto_encontrado

@tool
def consultar_web_colegio() -> str:
    """
    Utiliza esta herramienta EXCLUSIVAMENTE cuando necesites buscar información de contacto, 
    teléfonos, correos electrónicos, dirección o información general del colegio.
    """
    url = "https://www.redwoodcollege.cl/" 
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        
        # Extraemos el texto
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        texto_limpio = soup.get_text(separator=' ', strip=True)
        
        # --- CHISMÓGRAFO PARA LA TERMINAL ---
        print("\n" + "="*40)
        print("🕵️‍♂️ EL AGENTE LEYÓ ESTO DE LA WEB:")
        print(texto_limpio[:500]) 
        print("="*40 + "\n")
        
        if len(texto_limpio) < 50:
            return "Error: Pude entrar a la web, pero el texto está oculto o protegido."
            
        return f"Información extraída de la web oficial: {texto_limpio[:3000]}"
        
    except Exception as e:
        print(f"\n❌ ERROR AL NAVEGAR: {e}\n")
        return f"No se pudo acceder a la página web. Error: {e}"