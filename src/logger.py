import json
import os
from datetime import datetime

# Archivo donde guardaremos el historial de rendimiento
LOG_FILE = "agent_logs.json"

def registrar_metrica(pregunta: str, latencia_segundos: float, tokens_totales: int, hubo_error: bool = False):
    """
    Guarda las métricas de observabilidad de cada ejecución del agente.
    """
    nuevo_registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "pregunta": pregunta,
        "latencia_segundos": round(latencia_segundos, 2),
        "tokens_totales": tokens_totales,
        "exitoso": not hubo_error
    }

    # Cargamos los logs antiguos si existen
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            pass

    # Agregamos el nuevo y guardamos
    logs.append(nuevo_registro)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)