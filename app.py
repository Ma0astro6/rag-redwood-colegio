import streamlit as st

st.set_page_config(page_title="Asistente Redwood", page_icon="🌲")

st.title("🤖 Asistente Virtual - Colegio Redwood")
st.write("Hola, soy el asistente del colegio. ¿En qué te puedo ayudar hoy?")

# Caja de chat simple
pregunta = st.text_input("Escribe tu duda aquí:")

if st.button("Enviar"):
    if pregunta:
        # Aquí iría la conexión real con LangChain en el futuro
        st.success(f"Recibí tu pregunta: '{pregunta}'. (El motor RAG está en construcción).")
    else:
        st.warning("Por favor, escribe una pregunta primero.")