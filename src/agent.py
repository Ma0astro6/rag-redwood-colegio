from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from src.tools import buscar_en_documentos, consultar_web_colegio

def inicializar_agente(api_key: str):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    # Entregarle las herramientas actualizadas
    tools = [buscar_en_documentos, consultar_web_colegio]

    system_prompt = (
         "Eres el Asistente Virtual Oficial del Colegio Redwood. "
         "Responde siempre en español, de forma amable, directa y concisa. "
         "REGLA 1: Si te preguntan por reglamentos, listas de útiles o lecturas complementarias, "
         "utiliza SIEMPRE la herramienta 'buscar_en_documentos'. "
         "REGLA 2: Si te preguntan por información de contacto o ubicación, "
         "utiliza la herramienta 'consultar_web_colegio'. "
         "REGLA 3: Nunca menciones explícitamente el nombre de las herramientas. Solo entrega la respuesta. "
         "REGLA 4: Si te saludan, responde el saludo amablemente sin usar herramientas. "
         "REGLA 5: Si preguntan cosas fuera de contexto, di que tu función es solo asistir con temas del colegio. "
         "REGLA 6: Nunca inventes datos. Si no encuentras la info, di que no la tienes. "
         "REGLA 7: CONFÍA EN TU HERRAMIENTA. Si la herramienta te devuelve información, entrégala al usuario sin dudar. "
         "Si el usuario te pide información de un curso usando números (ej: '1'), tradúcelo mentalmente a 'Primero Básico' antes de buscar."
    )

    agente = create_react_agent(llm, tools, prompt=system_prompt)
    return agente

    # 4. Construir el Agente usando LangGraph (Arquitectura state-of-the-art)
    agente = create_react_agent(llm, tools, prompt=system_prompt)

    return agente