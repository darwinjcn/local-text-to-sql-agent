# agente_herramienta_custom.py
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 1. Configuramos el modelo local
local_llm = LLM(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)

# 2. ¡CREAMOS NUESTRA PROPIA HERRAMIENTA! (Sin dependencias externas)
@tool("Calculadora de Crecimiento Porcentual")
def calcular_crecimiento(valor_inicial: float, valor_final: float) -> str:
    """Calcula el porcentaje de crecimiento entre dos valores numéricos. 
    Útil para análisis de ventas y métricas de negocio."""
    if valor_inicial == 0:
        return "El valor inicial no puede ser cero."
    crecimiento = ((valor_final - valor_inicial) / valor_inicial) * 100
    return f"El crecimiento es del {crecimiento:.2f}%"

# 3. Definimos al AGENTE (Ahora con nuestra herramienta)
analista = Agent(
    role="Analista de Datos Senior",
    goal="Analizar datos de ventas y calcular métricas de crecimiento con precisión absoluta, sin alucinar números.",
    backstory=(
        "Eres un experto en análisis de datos. No adivinas los números ni haces cálculos mentales; "
        "siempre usas tus herramientas de cálculo programadas para garantizar que cada porcentaje sea matemáticamente exacto."
    ),
    llm=local_llm,
    tools=[calcular_crecimiento],  # <--- Aquí inyectamos nuestra herramienta custom
    verbose=True
)

# 4. Definimos la TAREA (Forzamos al agente a usar la herramienta)
tarea_analisis = Task(
    description=(
        "Nuestros datos de ingresos por ventas de laptops son:\n"
        "- Enero: $75,000\n"
        "- Febrero: $60,000\n"
        "- Marzo: $110,000\n\n"
        "INSTRUCCIONES:\n"
        "PASO 1: Usa tu herramienta 'Calculadora de Crecimiento Porcentual' para calcular:\n"
        "   a) El crecimiento (o caída) de Enero a Febrero.\n"
        "   b) El crecimiento de Febrero a Marzo.\n"
        "PASO 2: Redacta un reporte ejecutivo explicando qué significan estos números."
    ),
    expected_output=(
        "Un reporte en Markdown que incluya:\n"
        "1. Los resultados exactos devueltos por tu herramienta de cálculo.\n"
        "2. Un análisis breve de la tendencia (la caída inicial y la posterior recuperación)."
    ),
    agent=analista
)

# 5. Ejecutamos el Crew
crew = Crew(
    agents=[analista],
    tasks=[tarea_analisis],
    process=Process.sequential
)

print("\n🚀 Iniciando el agente con herramienta personalizada...\n")
resultado = crew.kickoff()

print("\n" + "="*60)
print("📊 RESULTADO FINAL DEL AGENTE:")
print("="*60)
print(resultado.raw)