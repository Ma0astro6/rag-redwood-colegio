import streamlit as st
from typing import Literal
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from src.tools import buscar_en_documentos, consultar_web_colegio
from src.prompts import SYSTEM_PROMPT

@st.cache_resource 
def inicializar_agente(api_key: str):
    # 1. El Cerebro (LLM)
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile", 
        temperature=0
    )

    # 2. Preparamos las herramientas
    tools = [buscar_en_documentos, consultar_web_colegio]
    llm_con_herramientas = llm.bind_tools(tools)
    nodo_herramientas = ToolNode(tools)

    # 3. NODO 1: La función que hace pensar a la IA
    def llamar_modelo(state: MessagesState):
        mensajes = state["messages"]
        # Inyectamos el System Prompt al principio de la memoria
        if not mensajes or not isinstance(mensajes[0], SystemMessage):
            mensajes = [SystemMessage(content=SYSTEM_PROMPT)] + mensajes
        
        respuesta = llm_con_herramientas.invoke(mensajes)
        return {"messages": [respuesta]}

    # 4. ENRUTADOR: El semáforo condicional
    def deberia_continuar(state: MessagesState) -> Literal["tools", "__end__"]:
        ultimo_mensaje = state["messages"][-1]
        # Si la IA decidió usar una herramienta, mandamos el flujo al nodo de herramientas
        if ultimo_mensaje.tool_calls:
            return "tools"
        # Si no, terminamos y mostramos la respuesta al usuario
        return "__end__"

    # 5. 🚀 ARMADO DEL GRAFO 
    workflow = StateGraph(MessagesState)

    # Agregamos los nodos principales
    workflow.add_node("agent", llamar_modelo)
    workflow.add_node("tools", nodo_herramientas)

    # Dibujamos las flechas (Edges) lógicas
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", deberia_continuar)
    workflow.add_edge("tools", "agent")

    # 6. Compilamos el grafo con memoria cognitiva
    memoria = MemorySaver()
    agente_compilado = workflow.compile(checkpointer=memoria)
    
    return agente_compilado