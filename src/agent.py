from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver 
from src.tools import buscar_en_documentos, consultar_web_colegio
from src.prompts import SYSTEM_PROMPT 

def inicializar_agente(api_key: str):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile", 
        temperature=0
    )

    tools = [buscar_en_documentos, consultar_web_colegio]
    
    # Activamos el guardado de memoria
    memoria = MemorySaver()

    # Le pasamos la memoria al agente
    agente = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT, checkpointer=memoria)
    return agente