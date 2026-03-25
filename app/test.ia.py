from google import genai

# Usamos tu API KEY
client = genai.Client(api_key="AIzaSyDZpH3UaYWbzAuMKQYeX3QMq6PpMp4639E")

try:
    # Usamos uno de los modelos que tu lista confirmó como disponibles
    # 'gemini-3-flash-preview' es excelente para análisis rápido
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents="Hola, ahora sí estamos usando un modelo disponible. ¿Qué tal?"
    )
    print("✅ ¡CONEXIÓN EXITOSA!")
    print(f"Respuesta de Gemini: {response.text}")

except Exception as e:
    print(f"❌ Error detectado: {e}")