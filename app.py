import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from src.agent import inicializar_agente

# 1. Configuración de la página
st.set_page_config(page_title="Agente Redwood", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Agente Inteligente con Tools - Redwood")

# 2. Configuración de la Memoria (IE3 e IE4)
# Aquí separamos la memoria visual (para ti) de la memoria cognitiva (para la IA)
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [] # Lo que se ve en pantalla
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # El cerebro del agente que recuerda el contexto

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
                    # Al invocar en LangGraph, le pasamos TODO el historial de una vez
                    respuesta = agente_ejecutor.invoke({"messages": st.session_state.chat_history})
                    
                    # Extraer el último mensaje (la respuesta de la IA)
                    mensaje_ia = respuesta["messages"][-1]
                    texto_respuesta = mensaje_ia.content
                    
                    st.markdown(texto_respuesta)
                    
                    # Guardar respuesta visual
                    st.session_state.mensajes.append({"role": "assistant", "content": texto_respuesta})
                    
                    # Guardar en la Memoria Cognitiva (Para cumplir IE3 e IE4)
                    st.session_state.chat_history.append(mensaje_ia)

                except Exception as e:
                    st.error(f"Error en la ejecución del Agente: {e}")
else:
    st.warning("👈 Por favor, ingresa tu API Key de Groq para despertar al Agente.")