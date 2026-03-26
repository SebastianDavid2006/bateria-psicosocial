import google.generativeai as genai
import streamlit as st

def consultar_gemini(prompt_usuario):
    """
    Se conecta con la API de Gemini para generar recomendaciones 
    basadas en los datos psicosociales.
    """
    # Intentar obtener la API KEY desde los secretos de Streamlit o variables de entorno
    # Si estás en local, puedes ponerla directamente: api_key = "TU_API_KEY"
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyCvjEW0fLeBgWFRJUq8m_8m10NDoxDZB3o")
    
    if api_key == "TU_API_KEY_AQUI":
        return "⚠️ Error: No se configuró la API Key de Gemini."

    try:
        # Configurar el modelo
        genai.configure(api_key=api_key)
        
        # Configuración de generación para que las respuestas sean profesionales y concisas
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 1024,
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Usamos Flash por ser más rápido para recomendaciones
            generation_config=generation_config,
        )

        # Prompt de sistema implícito para darle rol a la IA
        contexto_instruccion = (
            "Actúa como un experto en Psicología Organizacional y Seguridad y Salud en el Trabajo (SST). "
            "Tus recomendaciones deben ser técnicas, basadas en la normativa de riesgos psicosociales, "
            "pero fáciles de implementar en una empresa. Responde de forma estructurada con viñetas.\n\n"
        )

        response = model.generate_content(contexto_instruccion + prompt_usuario)
        
        return response.text

    except Exception as e:
        return f"❌ Error al consultar la IA: {str(e)}"