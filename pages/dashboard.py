import streamlit as st
import pandas as pd
import json
import os

# Configuración de la página
st.set_page_config(page_title="Dashboard Redwood", page_icon="📊", layout="wide")
st.title("📊 Panel de Observabilidad y Métricas")
st.markdown("Monitoreo en tiempo real del Agente RAG Redwood")
st.markdown("---")

LOG_FILE = "agent_logs.json"

if os.path.exists(LOG_FILE):
    # Cargar los datos
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    # 1. KPIs (Métricas Clave)
    st.subheader("📈 Indicadores Generales")
    col1, col2, col3, col4 = st.columns(4)
    
    total_consultas = len(df)
    latencia_promedio = df["latencia_segundos"].mean()
    max_tokens = df["tokens_totales"].max()
    tasa_exito = (df["exitoso"].sum() / total_consultas) * 100

    col1.metric("Total Consultas", total_consultas)
    col2.metric("Latencia Promedio", f"{latencia_promedio:.2f} s")
    col3.metric("Pico de Tokens", max_tokens)
    col4.metric("Tasa de Éxito", f"{tasa_exito:.1f}%")

    st.markdown("---")

    # 2. Gráficos Visuales
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("⏱️ Latencia por Consulta (Segundos)")
        st.line_chart(df["latencia_segundos"])

    with col_graf2:
        st.subheader("🪙 Consumo de Tokens (Memoria Cognitiva)")
        st.bar_chart(df["tokens_totales"])

    st.markdown("---")

    # 3. Trazabilidad de Logs
    st.subheader("📋 Registro Detallado de Trazabilidad (Logs)")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ No se encontró el archivo de logs. Ve a la página principal y hazle preguntas al agente para generar datos.")