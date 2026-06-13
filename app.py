import streamlit as st
import uuid
from langchain_core.messages import AIMessage, HumanMessage
from src.agent import inicializar_agente
import time
from src.logger import registrar_metrica 

# 1. Configuración de la página
st.set_page_config(page_title="Agente Redwood", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Agente Inteligente con Tools - Redwood")

# 2. Configuración de la Memoria
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [] 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4()) 

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
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")

    # 5. Dibujar el chat en pantalla
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # 6. Interacción: Cuando el usuario escribe algo
    if prompt := st.chat_input("Escribe tu consulta..."):
        # 1. Mostramos el mensaje del usuario (AHORA SÍ CON INDENTACIÓN)
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Iniciamos el cronómetro ⏱
        inicio_tiempo = time.time()
        hubo_error = False
        tokens_usados = 0

        with st.chat_message("assistant"):
            try:
                #  Llamamos al agente (Corrección: agente_ejecutor y thread_id dinámico)
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                respuesta_agente = agente_ejecutor.invoke({"messages": [("user", prompt)]}, config)
                
                # Extraemos el mensaje final
                ultimo_mensaje = respuesta_agente["messages"][-1]
                respuesta_texto = ultimo_mensaje.content
                
                # EXTRAEMOS LA MÉTRICA DE TOKENS (Uso de recursos)
                if hasattr(ultimo_mensaje, 'response_metadata'):
                    tokens_usados = ultimo_mensaje.response_metadata.get("token_usage", {}).get("total_tokens", 0)

                st.markdown(respuesta_texto)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta_texto})
                
            except Exception as e:
                hubo_error = True
                st.error(f"Error de conexión: {e}")
                respuesta_texto = f"Error: {e}"

        # 3. Detenemos el cronómetro y calculamos latencia 
        fin_tiempo = time.time()
        latencia = fin_tiempo - inicio_tiempo

        # 4. Guardamos todo en nuestro archivo de logs silenciosamente 
        registrar_metrica(
            pregunta=prompt,
            latencia_segundos=latencia,
            tokens_totales=tokens_usados,
            hubo_error=hubo_error
        )
else:
    st.warning("👈 Por favor, ingresa tu API Key de Groq para despertar al Agente.")