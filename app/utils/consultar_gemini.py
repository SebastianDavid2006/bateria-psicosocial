import os
import time
from typing import Any, Dict, List, Optional

import google.generativeai as genai

DEFAULT_GEMINI_MODELS: List[str] = [
    "models/gemini-3.1-pro",
    "models/gemini-2.5-pro",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-002",
    "models/gemini-3.1",
    "models/gemini-2.5",
    "models/gemini-1.5",
    "models/text-bison-002",
    "models/text-bison-001",
]


def _list_available_models() -> List[str]:
    try:
        models = genai.list_models()
        result: List[str] = []
        for model in models:
            if hasattr(model, "name"):
                result.append(model.name)
            elif isinstance(model, str):
                result.append(model)
        return result
    except Exception:
        return []


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


def _normalize_model_name(modelo: str) -> str:
    return modelo if modelo.startswith("models/") else f"models/{modelo}"


def _get_model_list(available_models: Optional[List[str]] = None) -> List[str]:
    env_model = os.getenv("GENAI_MODEL")
    normalized = _normalize_model_name(env_model) if env_model else None

    if available_models:
        modelos = []
        if normalized:
            modelos.append(normalized)
        for model in available_models:
            if model not in modelos:
                modelos.append(model)
        return modelos

    if normalized:
        return [normalized] + [m for m in DEFAULT_GEMINI_MODELS if m != normalized]
    return DEFAULT_GEMINI_MODELS


def _configure_genai(api_key: str) -> None:
    genai.configure(api_key=api_key, transport="rest")


def _build_prompt(prompt_usuario: str, config: Dict[str, Any]) -> str:
    return _build_system_prompt(config) + prompt_usuario.strip()


def _parse_response(response: Any) -> Optional[str]:
    if hasattr(response, "text") and isinstance(response.text, str) and response.text.strip():
        return response.text.strip()

    if hasattr(response, "candidates") and response.candidates:
        primera = response.candidates[0]
        content = getattr(primera, "content", None)
        if isinstance(content, dict):
            parts = content.get("parts", [])
            if parts and isinstance(parts, list):
                texto = parts[0].get("text", "")
                if texto:
                    return texto.strip()
        if hasattr(content, "text") and isinstance(content.text, str) and content.text.strip():
            return content.text.strip()

        output = getattr(primera, "output", None)
        if isinstance(output, str) and output.strip():
            return output.strip()
        if isinstance(output, dict):
            texto = output.get("text", "")
            if texto:
                return texto.strip()

    return None


def _try_model(modelo: str, prompt: str, max_tokens: int) -> str:
    model = genai.GenerativeModel(model_name=modelo)
    generation_config = genai.GenerationConfig(
        temperature=0.5,
        top_p=0.95,
        top_k=20,
        max_output_tokens=max_tokens,
    )
    response = model.generate_content(prompt, generation_config=generation_config)
    parsed = _parse_response(response)
    if parsed:
        return parsed
    raise RuntimeError("Respuesta de Gemini sin texto válido.")


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

    _configure_genai(api_key)
    prompt = _build_prompt(prompt_usuario, config)

    available_models = _list_available_models()
    modelos = _get_model_list(available_models)
    errores: List[str] = []

    if available_models:
        errores.append(f"Modelos disponibles detectados: {', '.join(available_models[:8])}...")

    for modelo in modelos:
        try:
            return _try_model(modelo, prompt, max_tokens)
        except Exception as e:
            mensaje = str(e).strip()
            if "401" in mensaje or "403" in mensaje:
                return "❌ Error de autenticación: verifica tu API key de Google AI."
            errores.append(f"{modelo} -> {mensaje}")
            time.sleep(1)

    detalles = "\n".join(errores[-8:])
    return (
        "❌ No se pudo conectar con ningún modelo de Gemini. Revisa tu API key, el modelo y el acceso de tu cuenta.\n"
        f"Intentos recientes:\n{detalles}"
    )
