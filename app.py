import streamlit as st
import uuid
from langchain_core.messages import AIMessage, HumanMessage
from src.agent import inicializar_agente

# 1. Configuración de la página
st.set_page_config(page_title="Agente Redwood", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Agente Inteligente con Tools - Redwood")

# 2. Configuración de la Memoria
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [] 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4()) # 🚀 NUEVO: ID de sesión único

# 3. Barra lateral
st.sidebar.header("⚙️ Configuración del Sistema")
groq_api_key = st.sidebar.text_input("Ingresa tu Groq API Key", type="password")

if groq_api_key:
    # 4. Conectar el Frontend con el Backend Lógico
    with st.spinner("Despertando al agente y cargando herramientas..."):
        agente_ejecutor = inicializar_agente(groq_api_key)
    st.success("¡Agente operativo! Base vectorial y herramientas cargadas.")

    # Botón de limpieza de memoria
    if st.sidebar.button("🗑️ Resetear Memoria del Agente"):
        st.session_state.mensajes = []
        st.session_state.chat_history = []
        st.session_state.thread_id = str(uuid.uuid4()) # 🚀 ¡Mata la memoria vieja y crea una nueva!
        st.rerun()

    st.markdown("---")

    # 5. Dibujar el chat en pantalla
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # 6. Interacción: Cuando el usuario escribe algo
    if pregunta := st.chat_input("Escribe tu consulta o saluda al agente..."):
        
        # Mostrar la pregunta visualmente
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)

        # Preparar la memoria cognitiva para LangGraph
        st.session_state.chat_history.append(HumanMessage(content=pregunta))

        # El Agente evalúa, decide usar herramientas y responde
        with st.chat_message("assistant"):
            with st.spinner("Pensando y tomando decisiones..."):
                try:
                    config_memoria = {"configurable": {"thread_id": st.session_state.thread_id}}
                    
                    respuesta = agente_ejecutor.invoke(
                        {"messages": [HumanMessage(content=pregunta)]}, 
                        config_memoria
                    )
                    
                    mensaje_ia = respuesta["messages"][-1]
                    texto_respuesta = mensaje_ia.content
                    
                    st.markdown(texto_respuesta)
                    st.session_state.mensajes.append({"role": "assistant", "content": texto_respuesta})

                except Exception as e:
                    st.error(f"Error en la ejecución del Agente: {e}")
else:
    st.warning("👈 Por favor, ingresa tu API Key de Groq para despertar al Agente.")