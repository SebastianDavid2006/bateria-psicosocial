import os
import time
import requests
from typing import Any, Dict, List, Optional

DEFAULT_GEMINI_MODELS: List[str] = [
    "gemini-3.1-pro",
    "gemini-2.5-pro",
    "gemini-1.5-pro",
    "gemini-3.1",
    "gemini-2.5",
    "gemini-1.5",
    "gemini-1.0",
]


def _build_system_prompt(config: Dict[str, Any]) -> str:
    return (
        "Actúa como un experto senior en Psicología Organizacional y Seguridad y Salud en el Trabajo (SST).\n"
        "REGLAS CRÍTICAS DE RESPUESTA:\n"
        f"- Formato solicitado: {config['formato']}.\n"
        f"- Tono de comunicación: {config['tono']}.\n"
        f"- Extensión máxima: {config['max_palabras']} palabras.\n"
        "- No incluyas introducciones innecesarias.\n"
        "- Basa tus recomendaciones en normativas de riesgo psicosocial vigentes.\n\n"
        "DATOS PARA ANALIZAR:\n"
    )


def _get_model_list() -> List[str]:
    env_model = os.getenv("GENAI_MODEL")
    if env_model:
        return [env_model] + [m for m in DEFAULT_GEMINI_MODELS if m != env_model]
    return DEFAULT_GEMINI_MODELS


def _build_payload(prompt_usuario: str, config: Dict[str, Any], max_tokens: int, method: str) -> Dict[str, Any]:
    prompt_text = _build_system_prompt(config) + prompt_usuario

    if method == "generateContent":
        return {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.5,
                "topP": 0.95,
                "topK": 20,
                "maxOutputTokens": max_tokens,
            },
        }

    return {
        "prompt": {"text": prompt_text},
        "temperature": 0.5,
        "topP": 0.95,
        "topK": 20,
        "maxOutputTokens": max_tokens,
    }


def _call_gemini(modelo: str, api_key: str, payload: Dict[str, Any], method: str) -> requests.Response:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:{method}?key={api_key}"
    return requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )


def consultar_gemini(prompt_usuario: str, config_personalizada: Optional[Dict[str, Any]] = None, max_tokens: int = 10000) -> str:
    """Consulta a la API de Gemini manteniendo tus prompts originales."""
    config: Dict[str, Any] = {
        "formato": "Lista de viñetas",
        "tono": "Profesional y Técnico",
        "max_palabras": 150,
    }
    if config_personalizada:
        config.update(config_personalizada)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "❌ Error: variable de entorno GOOGLE_API_KEY no configurada."

    modelos = _get_model_list()
    metodos = ["generateContent", "generateText"]
    ultimo_error = "❌ Error: No se pudo conectar con ningún modelo de Gemini."

    for modelo in modelos:
        for metodo in metodos:
            try:
                payload = _build_payload(prompt_usuario, config, max_tokens, metodo)
                response = _call_gemini(modelo, api_key, payload, metodo)

                if response.status_code == 200:
                    data = response.json()
                    candidatos = data.get("candidates", [])
                    if candidatos and isinstance(candidatos, list):
                        primera = candidatos[0]
                        content = primera.get("content", {})
                        if isinstance(content, dict):
                            parts = content.get("parts", [])
                            if parts and isinstance(parts, list):
                                texto = parts[0].get("text", "")
                                if texto:
                                    return texto.strip()
                        output = primera.get("output")
                        if isinstance(output, str) and output.strip():
                            return output.strip()
                        if isinstance(output, dict):
                            texto = output.get("text", "")
                            if texto:
                                return texto.strip()
                    ultimo_error = "❌ Error: respuesta de Gemini malformada."
                    continue

                if response.status_code == 404:
                    ultimo_error = f"❌ Modelo {modelo} no disponible para {metodo}."
                    continue
                if response.status_code == 403:
                    return "❌ Error de autenticación: verifica tu API key de Google AI."
                if response.status_code == 429:
                    time.sleep(2)
                    continue

                ultimo_error = f"❌ Error API {response.status_code}: {response.text}"
            except requests.exceptions.Timeout:
                ultimo_error = "❌ Timeout al consultar la API de Gemini."
                continue
            except requests.exceptions.RequestException as e:
                ultimo_error = f"❌ Error de red al consultar Gemini: {e}"
                continue
            except Exception as e:
                ultimo_error = f"❌ Error inesperado: {e}"
                continue

    return ultimo_error
