import requests
import os

def consultar_gemini(prompt_usuario, config_personalizada=None, tokens=500):
    """
    Se conecta con la API de Gemini usando solicitudes HTTP.
    """
    try:
        # 1. Configuración de API
        api_key = "AIzaSyCrgZ00tWBTX7WpsX7oNmvC-hEoRM5APes"
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=" + api_key

        # 2. Extraer parámetros del usuario o usar valores por defecto
        formato = config_personalizada.get("formato", "Lista de viñetas") if config_personalizada else "Lista de viñetas"
        tono = config_personalizada.get("tono", "Profesional y Técnico") if config_personalizada else "Profesional y Técnico"
        max_palabras = config_personalizada.get("max_palabras", 150) if config_personalizada else 150

        # 3. Prompt de Sistema Dinámico
        instrucciones_sistema = (
            f"Actúa como un experto senior en Psicología Organizacional y Seguridad y Salud en el Trabajo (SST).\n"
            f"REGLAS CRÍTICAS DE RESPUESTA:\n"
            f"- Formato solicitado: {formato}.\n"
            f"- Tono de comunicación: {tono}.\n"
            f"- Extensión máxima: {max_palabras} palabras.\n"
            f"- No incluyas introducciones innecesarias.\n"
            f"- Basa tus recomendaciones en normativas de riesgo psicosocial vigentes.\n\n"
        )

        # 4. Construcción del cuerpo de la solicitud
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": instrucciones_sistema + "DATOS PARA ANALIZAR:\n" + prompt_usuario}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.5,
                "topP": 0.95,
                "topK": 20,
                "maxOutputTokens": tokens
            }
        }

        # 5. Enviar solicitud
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            # Extraer texto de la respuesta
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ Error al consultar la IA: {response.status_code} {response.text}"

    except Exception as e:
        return f"❌ Error al consultar la IA: {str(e)}"
