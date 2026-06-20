import json
import os
from datetime import datetime

LOG_FILE = "agent_logs.json"

# Variable global temporal para guardar los pasos del agente 
trazas_temporales = []

def registrar_tool_trace(nombre_tool: str, argumentos: dict, respuesta: str, latencia_tool: float):
    """Guarda los detalles internos cada vez que el agente usa una herramienta."""
    trazas_temporales.append({
        "herramienta_invocada": nombre_tool,
        "argumentos_usados": argumentos,
        "respuesta_herramienta": respuesta[:150] + "... [truncado]", # Cortamos texto largo para no saturar el JSON
        "tiempo_ejecucion_segundos": round(latencia_tool, 2)
    })

def registrar_metrica(pregunta: str, latencia_segundos: float, tokens_totales: int, hubo_error: bool = False):
    """Guarda la métrica final de la consulta completa."""
    global trazas_temporales
    
    nuevo_registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "pregunta_usuario": pregunta,
        "latencia_total_segundos": round(latencia_segundos, 2),
        "tokens_totales": tokens_totales,
        "exitoso": not hubo_error,
        "trazabilidad_interna": trazas_temporales # AQUÍ METEMOS EL REGISTRO DE LAS TOOLS
    }

    # Cargamos los logs antiguos si existen
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            pass

    logs.append(nuevo_registro)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
        
    # Limpiamos la memoria temporal para la siguiente pregunta del usuario
    trazas_temporales = []