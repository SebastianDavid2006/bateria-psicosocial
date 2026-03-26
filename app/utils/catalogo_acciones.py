# utils/catalogo_acciones.py

def obtener_nivel_riesgo_colombia(porcentaje):
    """
    Clasifica el riesgo basado EXACTAMENTE en la tabla 
    de baremos de la imagen del usuario.
    Retorna: (Nivel de Riesgo, Color Hexadecimal)
    """
    if porcentaje < 30:
        return "SIN RIESGO", "#006400" # Verde oscuro
    elif porcentaje < 50:
        return "BAJO", "#00FF00"      # Verde claro
    elif porcentaje < 70:
        return "MEDIO", "#FFFF00"     # Amarillo
    elif porcentaje < 85:
        return "ALTO", "#FF0000"      # Rojo (Para el borde)
    else:
        return "MUY ALTO", "#8B0000"  # Rojo oscuro

# Catálogo de acciones basado en tu imagen image_5bc161.png
CATALOGO_OFICIAL_ACCIONES = {
    "Demandas emocionales": {
        "MUY ALTO": "Seguimiento a inspecciones de EPP, Gestión emocional - Psicokeratty grupal.",
        "ALTO": "Intervención focalizada en gestión de emociones y talleres de contención emocional (SST).",
        "MEDIO": "Capacitación en manejo de usuarios difíciles y asertividad.",
        "BAJO": "Cápsulas informativas sobre bienestar emocional.",
        "SIN RIESGO": "Monitoreo preventivo semestral."
    },
    # ... agregar otras dimensiones después
}

def obtener_accion_y_contexto(dimension, puntaje):
    """
    Combina la lógica de baremos con el catálogo de acciones.
    """
    nivel, color = obtener_nivel_riesgo_colombia(puntaje)
    
    # Busca la acción oficial, si no existe devuelve un mensaje genérico
    accion_oficial = CATALOGO_OFICIAL_ACCIONES.get(dimension, {}).get(nivel, "Seguir lineamientos generales del SG-SST.")
    
    return nivel, accion_oficial, color