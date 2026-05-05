import streamlit as st
import PyPDF2
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader

# 1. Configuración de la página
st.set_page_config(page_title="Asistente Redwood (Groq)", page_icon="🌲")
st.title("Asistente Virtual RAG - Colegio Redwood")

# --- Inicializar memoria de chat (Session State) ---
# Esto es el "caché" que se borra al cerrar la app
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# 2. Barra lateral para la API Key
st.sidebar.header("⚙️ Configuración")
groq_api_key = st.sidebar.text_input("Ingresa tu Groq API Key", type="password")

# El nombre exacto de tu archivo PDF en la carpeta
nombre_archivo_pdf = "reglamento.pdf"

if groq_api_key:
    if os.path.exists(nombre_archivo_pdf):
        with st.spinner("Preparando el cerebro de la IA..."):
            
            # 3. Leer el PDF local
            texto_completo = ""
            with open(nombre_archivo_pdf, "rb") as archivo:
                lector = PyPDF2.PdfReader(archivo)
                for pagina in lector.pages:
                    texto_completo += pagina.extract_text() or ""
            
            # --- Leer la página web ---
            url_colegio = "https://www.redwoodcollege.cl/" 
            try:
                loader = WebBaseLoader(url_colegio)
                docs_web = loader.load()
                for doc in docs_web:
                    texto_completo += "\n\n" + doc.page_content
                st.toast("✅ Web del colegio leída con éxito")
            except Exception as e:
                st.toast(f"⚠️ No se pudo leer la web, usando solo el PDF. Error: {e}")
            
            # 4. Pipeline RAG: Chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            chunks = text_splitter.split_text(texto_completo)
            
            # 5. Embeddings GRATIS (HuggingFace) y Base Vectorial (FAISS)
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_texts(chunks, embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            # 6. System Prompt
            system_prompt = (
                "Actúa como un asistente administrativo experto del Colegio Redwood. "
                "Responde de forma clara, en español y utilizando ÚNICAMENTE el siguiente contexto extraído de los documentos oficiales. "
                "Si la respuesta no está en el contexto, di amablemente que no tienes esa información. "
                "Contexto oficial:\n{context}"
            )
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            # 7. Orquestador (LCEL) y Modelo LLM GRATIS
            llm = ChatGroq(
                groq_api_key=groq_api_key, 
                model_name="llama-3.1-8b-instant", 
                temperature=0
            )
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain = (
                {"context": retriever | format_docs, "input": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

        # 8. Interfaz de Chat con Historial
        st.markdown("---")
        
        # Dibujar todos los mensajes guardados en el historial
        for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])

        # Input del usuario anclado abajo (estilo ChatGPT)
        if pregunta := st.chat_input("Escribe tu duda sobre el reglamento aquí:"):
            
            # Guardar y mostrar lo que preguntó el usuario
            st.session_state.mensajes.append({"role": "user", "content": pregunta})
            with st.chat_message("user"):
                st.markdown(pregunta)

            # Generar, mostrar y guardar la respuesta de la IA
            with st.chat_message("assistant"):
                with st.spinner("Pensando a la velocidad de la luz..."):
                    try:
                        respuesta = rag_chain.invoke(pregunta)
                        st.markdown(respuesta)
                        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                    except Exception as e:
                        st.error(f"Error con Groq: {e}")
                        
        # Botoncito extra para limpiar el chat a mano sin tener que recargar la página
        if len(st.session_state.mensajes) > 0:
            if st.sidebar.button("🗑️ Limpiar historial"):
                st.session_state.mensajes = []
                st.rerun()

    else:
        st.error(f"❌ No se encontró el archivo '{nombre_archivo_pdf}'. Por favor, asegúrate de que esté en la misma carpeta.")
else:
    st.warning("👈 Por favor, ingresa tu API Key de Groq en el menú lateral.")