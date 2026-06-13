import os
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Conexión a la nube 
MONGO_URI = "mongodb+srv://matias:redwood2026@cluster0.baqowbh.mongodb.net/?appName=Cluster0"

def get_vectorstore():
    """Inicializa y retorna la conexión a la base de datos vectorial."""
    try:
        # Conexión al cliente y colección
        cliente_mongo = MongoClient(MONGO_URI)
        coleccion_mongo = cliente_mongo["redwood_db"]["documentos"]
        
        # Modelo de embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Configuración del Vector Store
        vectorstore = MongoDBAtlasVectorSearch(
            collection=coleccion_mongo,
            embedding=embeddings,
            index_name="vector_index",
            text_key="text",           
            embedding_key="embedding"  
        )
        return vectorstore
    except Exception as e:
        print(f"❌ Error crítico conectando a MongoDB: {e}")
        return None