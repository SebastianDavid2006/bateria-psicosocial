# utils/catalogo_acciones.py

def obtener_diagnostico_completo(dimension, porcentaje):
    """
    Clasifica el riesgo y asigna la acción oficial.
    Basado en la Tabla de Baremos del usuario.
    """
    # 1. Lógica de Baremos (Basado en tu imagen de porcentajes)
    if porcentaje < 30:
        nivel, color = "SIN RIESGO", "#006400" # Verde oscuro
    elif porcentaje < 50:
        nivel, color = "BAJO", "#228B22"      # Verde bosque
    elif porcentaje < 70:
        nivel, color = "MEDIO", "#FFD700"     # Dorado/Amarillo
    elif porcentaje < 85:
        nivel, color = "ALTO", "#FF4500"      # Naranja/Rojo
    else:
        nivel, color = "MUY ALTO", "#8B0000"  # Rojo oscuro

    # 2. Catálogo de Acciones (Oficial)
    # Aquí iremos mapeando las 40 dimensiones
    catalogo_acciones = {
        "Demandas emocionales": {
            "MUY ALTO": "Seguimiento a inspecciones de EPP, Gestión emocional - Psicokeratty grupal e intervención clínica individual.",
            "ALTO": "Intervención focalizada en gestión de emociones y talleres de contención emocional (SST).",
            "MEDIO": "Capacitación en manejo de usuarios difíciles, asertividad y comunicación no violenta.",
            "BAJO": "Cápsulas informativas sobre bienestar emocional.",
            "SIN RIESGO": "Mantener actividades de promoción de la salud mental y monitoreo preventivo."
        }
    }

    # Buscamos la acción oficial en el diccionario
    accion = catalogo_acciones.get(dimension, {}).get(nivel, "Consultar manual general de SST para acciones específicas.")

    return nivel, color, accion