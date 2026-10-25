# test_conexion.py
from crewai import LLM

# 1. Configuramos la conexión a Ollama local
ollama_llm = LLM(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)

# 2. Hacemos una llamada directa al modelo para probar
print("Probando conexión con Ollama...")
respuesta = ollama_llm.call("Responde en una sola palabra: ¿Estás funcionando correctamente?")

print(f"\nRespuesta del modelo: {respuesta}")