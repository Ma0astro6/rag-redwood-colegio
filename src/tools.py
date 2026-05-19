import os
from langchain_core.tools import tool
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import docx
import requests
from bs4 import BeautifulSoup

# 1. Conexión a la nube (¡PEGA TU LINK AQUÍ Y CAMBIA EL <password>!)
MONGO_URI = "mongodb+srv://matias:redwood2026@cluster0.baqowbh.mongodb.net/?appName=Cluster0"

# Nos conectamos al servidor y a la colección exacta
cliente_mongo = MongoClient(MONGO_URI)
coleccion_mongo = cliente_mongo["redwood_db"]["documentos"]

# Preparamos el modelo de embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Enlazamos LangChain con MongoDB
vectorstore = MongoDBAtlasVectorSearch(
    collection=coleccion_mongo,
    embedding=embeddings,
    index_name="vector_index"
)

# 2. Carga Inteligente (Sube los archivos solo 1 vez)
try:
    if coleccion_mongo.count_documents({}) == 0:
        print("☁️ La base de datos está vacía. Subiendo documentos a la nube...")
        carpeta_public = "public"
        texto_completo = ""
        archivos_leidos = 0

        if os.path.exists(carpeta_public):
            for nombre_archivo in os.listdir(carpeta_public):
                ruta_archivo = os.path.join(carpeta_public, nombre_archivo)
                
                if nombre_archivo.endswith(".pdf"):
                    with open(ruta_archivo, "rb") as archivo:
                        lector = PyPDF2.PdfReader(archivo)
                        for pagina in lector.pages:
                            texto_completo += pagina.extract_text() or ""
                    archivos_leidos += 1
                    print(f"📄 Procesando PDF: {nombre_archivo}")
                    
                elif nombre_archivo.endswith(".docx") and not nombre_archivo.startswith("~$"):
                    doc = docx.Document(ruta_archivo)
                    for parrafo in doc.paragraphs:
                        texto_completo += parrafo.text + "\n"
                    archivos_leidos += 1
                    print(f"📝 Procesando Word: {nombre_archivo}")

            if archivos_leidos > 0:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300) 
                chunks = text_splitter.split_text(texto_completo)
                
                # ¡La magia! Se suben todos los vectores a MongoDB
                vectorstore.add_texts(chunks)
                print(f"✅ ¡Éxito! {archivos_leidos} documentos subidos y vectorizados en MongoDB.")
            else:
                print("⚠️ No hay documentos válidos en la carpeta public.")
        else:
            print("❌ No existe la carpeta public.")
    else:
        print("✅ Conexión exitosa a MongoDB. Los documentos ya estaban en la nube.")
except Exception as e:
    print(f"❌ Error de conexión con MongoDB: {e}")


# 3. LAS HERRAMIENTAS
@tool
def buscar_en_documentos(pregunta: str) -> str:
    """
    Utiliza esta herramienta SIEMPRE para buscar información sobre el reglamento, 
    listas de útiles, lecturas complementarias o profesores.
    """
    # Rastreador para la consola
    print(f"🚨 EL AGENTE ESTÁ BUSCANDO EN MONGO: {pregunta}") 
    
    docs = vectorstore.similarity_search(pregunta, k=5)
    contexto_encontrado = "\n\n".join(doc.page_content for doc in docs)
    return contexto_encontrado

@tool
def consultar_web_colegio() -> str:
    """
    Utiliza esta herramienta EXCLUSIVAMENTE cuando necesites buscar información de contacto, 
    teléfonos, correos electrónicos, dirección o información general del colegio.
    """
    # Rastreador para la consola
    print("🚨 EL AGENTE ESTÁ LEYENDO LA PÁGINA WEB OFICIAL") 
    
    url = "https://www.redwoodcollege.cl/contacto" 
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        texto_limpio = soup.get_text(separator=' ', strip=True)
        
        if len(texto_limpio) < 50:
            return "Error: Pude entrar a la web, pero el texto está oculto o protegido."
            
        return f"Información extraída de la web oficial: {texto_limpio[:3000]}"
        
    except Exception as e:
        return f"No se pudo acceder a la página web. Error: {e}"