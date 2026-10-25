# agente_csv_hibrido.py
import pandas as pd
from crewai import Agent, Task, Crew, Process, LLM

# 1. Configuramos el modelo local
local_llm = LLM(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)

# 2. PYTHON HACE EL TRABALO PESADO Y EXACTO (Determinístico)
df = pd.read_csv("ventas.csv")

# Cálculo A: Ingresos por producto
ingresos_prod = df.groupby("Producto")["Total"].sum().reset_index()
ingresos_prod = ingresos_prod.sort_values(by="Total", ascending=False)
top_producto = ingresos_prod.iloc[0]

# Cálculo B: Unidades por categoría
unidades_cat = df.groupby("Categoria")["Unidades"].sum().reset_index()
unidades_cat = unidades_cat.sort_values(by="Unidades", ascending=False)
top_categoria = unidades_cat.iloc[0]

# Cálculo C: Ingresos por mes
df["Mes"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m")
ingresos_mes = df.groupby("Mes")["Total"].sum().reset_index()
ingresos_mes = ingresos_mes.sort_values(by="Total", ascending=False)
top_mes = ingresos_mes.iloc[0]

# Creamos un string con LOS DATOS REALES Y VERIFICADOS
datos_reales = f"""
- Producto con más ingresos: {top_producto['Producto']} (${top_producto['Total']:,.2f})
- Categoría con más unidades: {top_categoria['Categoria']} ({top_categoria['Unidades']} unidades)
- Mes más rentable: {top_mes['Mes']} (${top_mes['Total']:,.2f})
"""

# 3. Definimos al AGENTE (Ahora su rol es solo REDACTAR, no calcular)
redactor_ejecutivo = Agent(
    role="Redactor Ejecutivo de Datos",
    goal="Tomar datos verificados y convertirlos en un reporte de negocios profesional, claro y persuasivo.",
    backstory=(
        "Eres un experto en comunicación de negocios. No tienes acceso a los datos crudos, "
        "solo recibes los hallazgos ya calculados y verificados por un equipo de ingeniería de datos. "
        "Tu trabajo es darles contexto, formato Markdown y una recomendación estratégica lógica."
    ),
    llm=local_llm,
    verbose=True
)

# 4. La TAREA recibe los datos YA calculados en el prompt
tarea_redaccion = Task(
    description=(
        "Un equipo de ingeniería de datos ha analizado el archivo 'ventas.csv' y te ha entregado estos hallazgos 100% verificados:\n\n"
        f"{datos_reales}\n\n"
        "Tu misión es redactar un reporte ejecutivo basado ÚNICAMENTE en estos tres puntos."
    ),
    expected_output=(
        "Un reporte en Markdown con:\n"
        "1. Un título profesional.\n"
        "2. Un resumen ejecutivo de 2 oraciones.\n"
        "3. Los 3 hallazgos presentados de forma clara y con los números exactos proporcionados.\n"
        "4. Una recomendación de negocio lógica basada en que el producto y mes mencionados son los mejores."
    ),
    agent=redactor_ejecutivo
)

# 5. Ejecutamos
crew = Crew(
    agents=[redactor_ejecutivo],
    tasks=[tarea_redaccion],
    process=Process.sequential
)

print("\n🚀 Iniciando Agente Híbrido (Cálculo en Python, Redacción en IA)...\n")
resultado = crew.kickoff()

print("\n" + "="*70)
print("📊 REPORTE FINAL (NÚMEROS 100% REALES):")
print("="*70)
print(resultado.raw)