# agente_sql.py
import sqlite3
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 1. Configuramos el modelo local
local_llm = LLM(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)

# 2. HERRAMIENTA: Ejecutar consultas SQL
@tool("Ejecutor de Consultas SQL")
def ejecutar_sql(query: str) -> str:
    """Recibe una consulta SQL SELECT y devuelve los resultados de la base de datos SQLite.
    IMPORTANTE: La base de datos tiene una tabla llamada 'ventas' con las columnas: 
    id, fecha (formato YYYY-MM-DD), producto, categoria, unidades, precio_unitario, total."""
    try:
        conn = sqlite3.connect("ventas.db")
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Obtener nombres de columnas
        columnas = [descripcion[0] for descripcion in cursor.description]
        
        # Formatear como tabla Markdown
        tabla = "| " + " | ".join(columnas) + " |\n"
        tabla += "| " + " | ".join(["---"] * len(columnas)) + " |\n"
        for fila in resultados:
            tabla += "| " + " | ".join(str(valor) for valor in fila) + " |\n"
        
        conn.close()
        
        if not resultados:
            return "La consulta no devolvió resultados."
        return f"Resultados ({len(resultados)} filas):\n{tabla}"
    except Exception as e:
        return f"❌ Error al ejecutar la consulta SQL: {str(e)}"

# 3. Definimos al AGENTE Text-to-SQL
analista_sql = Agent(
    role="Analista de Base de Datos SQL Senior",
    goal="Traducir preguntas de negocio en lenguaje natural a consultas SQL precisas, ejecutarlas y explicar los resultados.",
    backstory=(
        "Eres un experto en SQL y análisis de datos. "
        "Siempre generas consultas SQL válidas y seguras (solo SELECT). "
        "Explicas los resultados de forma clara y orientada al negocio."
    ),
    llm=local_llm,
    tools=[ejecutar_sql],
    verbose=True
)

# 4. La TAREA (Pregunta en lenguaje natural)
pregunta_usuario = "¿Cuál fue el producto que más ingresos generó en el mes de marzo de 2026 y cuántas unidades vendió en total?"

tarea_sql = Task(
    description=(
        f"El usuario te hace la siguiente pregunta:\n\n"
        f"'{pregunta_usuario}'\n\n"
        f"PASO 1: Analiza la pregunta y determina qué consulta SQL necesitas ejecutar.\n"
        f"PASO 2: Usa tu herramienta 'Ejecutor de Consultas SQL' para obtener los datos reales.\n"
        f"PASO 3: Interpreta los resultados y redacta una respuesta clara en español."
    ),
    expected_output=(
        "Una respuesta en texto plano que incluya:\n"
        "1. La consulta SQL que ejecutaste.\n"
        "2. Los resultados de forma clara.\n"
        "3. Una explicación concisa de lo que significan esos datos."
    ),
    agent=analista_sql
)

# 5. Ejecutamos
crew = Crew(
    agents=[analista_sql],
    tasks=[tarea_sql],
    process=Process.sequential
)

print("\n🚀 Iniciando Agente Text-to-SQL...\n")
print(f"📝 Pregunta del usuario: {pregunta_usuario}\n")
resultado = crew.kickoff()

print("\n" + "="*70)
print("💬 RESPUESTA DEL AGENTE:")
print("="*70)
print(resultado.raw)