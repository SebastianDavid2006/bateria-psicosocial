import google.generativeai as genai
import streamlit as st
import os 

def consultar_gemini(prompt_usuario, config_personalizada=None):
    """
    Se conecta con la API de Gemini. 
    Acepta 'config_personalizada' para ajustar el comportamiento dinámicamente.
    """
    
    try:
        # 1. Configuración de API
        # Nota: Idealmente usa st.secrets["GEMINI_API_KEY"] para producción
        api_key_uwu = "AIzaSyCrgZ00tWBTX7WpsX7oNmvC-hEoRM5APes" 
        genai.configure(api_key=api_key_uwu)
        
        # 2. Extraer parámetros del usuario o usar valores por defecto
        # Esto permite que lo que elijas en los selectores de Streamlit llegue aquí
        formato = config_personalizada.get("formato", "Lista de viñetas") if config_personalizada else "Lista de viñetas"
        tono = config_personalizada.get("tono", "Profesional y Técnico") if config_personalizada else "Profesional y Técnico"
        max_palabras = config_personalizada.get("max_palabras", 150) if config_personalizada else 150

        # 3. Configuración del modelo
        generation_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 20,
            "max_output_tokens": 3500, # Límite técnico de la respuesta
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", # Versión actualizada y eficiente
            generation_config=generation_config,
        )

        # 4. Prompt de Sistema Dinámico (Aquí es donde aplicamos tus parámetros)
        instrucciones_sistema = (
            f"Actúa como un experto senior en Psicología Organizacional y Seguridad y Salud en el Trabajo (SST).\n"
            f"REGLAS CRÍTICAS DE RESPUESTA:\n"
            f"- Formato solicitado: {formato}.\n"
            f"- Tono de comunicación: {tono}.\n"
            f"- Extensión máxima: {max_palabras} palabras.\n"
            f"- No incluyas introducciones innecesarias como 'Claro, aquí tienes...'. Ve directo al grano.\n"
            f"- Basa tus recomendaciones en normativas de riesgo psicosocial vigentes.\n\n"
        )

        # 5. Generación
        response = model.generate_content(instrucciones_sistema + "DATOS PARA ANALIZAR:\n" + prompt_usuario)
        
        return response.text

    except Exception as e:
        return f"❌ Error al consultar la IA: {str(e)}"