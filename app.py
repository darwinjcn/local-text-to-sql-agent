# app.py
import streamlit as st
import sqlite3
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 1. Configuración de la página
st.set_page_config(page_title="Local Text-to-SQL Agent", page_icon="🤖", layout="wide")

# 2. Barra Lateral (Sidebar) para información del proyecto
with st.sidebar:
    st.title("🤖 Agent Info")
    st.markdown("### 🛠️ Stack Tecnológico")
    st.markdown("- **CrewAI**: Orquestación de agentes")
    st.markdown("- **Ollama + Qwen 2.5 (7B)**: LLM Local")
    st.markdown("- **SQLite**: Base de datos relacional")
    st.markdown("- **Streamlit**: Interfaz Web")
    st.divider()
    st.markdown("### 📂 Base de Datos")
    st.info("Contiene ventas de Enero a Marzo de 2026.")
    st.caption("Desarrollado por Darwin Colmenares | 2026")

# 3. Título y descripción principal
st.title("🤖 Local Text-to-SQL Agent")
st.markdown("Haz una pregunta en lenguaje natural sobre las ventas y el agente consultará la base de datos SQLite en tiempo real, **sin alucinaciones**.")

# 4. Cargar el Agente en caché
@st.cache_resource
def cargar_agente():
    local_llm = LLM(
        model="ollama/qwen2.5:7b",
        base_url="http://localhost:11434"
    )

    @tool("Ejecutor de Consultas SQL")
    def ejecutar_sql(query: str) -> str:
        """Ejecuta una consulta SELECT en la base de datos 'ventas.db'. 
        La tabla 'ventas' tiene las columnas: id, fecha (YYYY-MM-DD), producto, categoria, unidades, precio_unitario, total.
        Los datos cubren el período de ENERO A MARZO DE 2026.
        IMPORTANTE: Siempre incluye las columnas numéricas (unidades, total) en tu SELECT."""
        try:
            conn = sqlite3.connect("ventas.db")
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            
            tabla = "| " + " | ".join(columnas) + " |\n"
            tabla += "| " + " | ".join(["---"] * len(columnas)) + " |\n"
            for fila in resultados:
                tabla += "| " + " | ".join(str(v) for v in fila) + " |\n"
            conn.close()
            
            return f"Resultados ({len(resultados)} filas):\n{tabla}" if resultados else "La consulta no devolvió resultados."
        except Exception as e:
            return f"❌ Error al ejecutar SQL: {str(e)}"

    analista = Agent(
        role="Analista de Base de Datos SQL Senior",
        goal="Responder preguntas de negocio ejecutando consultas SQL precisas y mostrando los datos reales en formato tabla.",
        backstory=(
            "Eres un experto en SQL y análisis de datos. "
            "NUNCA inventas números ni asumes datos que no existen. "
            "SIEMPRE ejecutas tu herramienta 'Ejecutor de Consultas SQL' antes de responder. "
            "La base de datos contiene ventas del período ENERO A MARZO DE 2026. "
            "Cuando generes un SELECT, SIEMPRE incluye las columnas numéricas relevantes "
            "(unidades, total) junto con las de agrupación (producto, categoria) para mostrar tablas completas."
        ),
        llm=local_llm,
        tools=[ejecutar_sql],
        verbose=False
    )

    tarea = Task(
        description=(
            "El usuario hace la siguiente pregunta: '{pregunta}'.\n\n"
            "CONTEXTO IMPORTANTE: Los datos en la base de datos son del año 2026 (enero, febrero y marzo).\n\n"
            "PASO 1: Analiza qué columnas necesita la respuesta.\n"
            "PASO 2: Genera una consulta SQL que INCLUYA tanto las columnas de agrupación como las numéricas.\n"
            "PASO 3: EJECUTA tu herramienta 'Ejecutor de Consultas SQL' con la consulta generada.\n"
            "PASO 4: Responde en español mostrando:\n"
            "   - La consulta SQL ejecutada (en bloque de código).\n"
            "   - Los resultados REALES devueltos por la herramienta en formato tabla.\n"
            "   - Una breve interpretación de los datos."
        ),
        expected_output=(
            "Respuesta en Markdown con:\n"
            "1. La consulta SQL ejecutada.\n"
            "2. Una tabla Markdown con los resultados REALES (no inventados).\n"
            "3. Una interpretación clara de los datos."
        ),
        agent=analista
    )

    return Crew(agents=[analista], tasks=[tarea], process=Process.sequential)

# 5. Interfaz de Usuario (Formulario)
st.info("💡 **Prueba con:** '¿Cuál fue el producto que más ingresos generó en marzo de 2026?' o '¿Cuánto se vendió en total por categoría?'")

with st.form("formulario_pregunta", clear_on_submit=True):
    pregunta_usuario = st.text_input(
        "Escribe tu pregunta aquí:", 
        placeholder="Ej: ¿Cuáles son los productos que menos se vendieron en marzo?",
        label_visibility="collapsed"
    )
    
    enviado = st.form_submit_button("🚀 Analizar Datos", type="primary")

    if enviado:
        if not pregunta_usuario.strip():
            st.warning("⚠️ Por favor, escribe una pregunta primero.")
        else:
            with st.spinner("🧠 El agente está pensando y consultando la base de datos..."):
                try:
                    # Medir el tiempo de ejecución
                    start_time = time.time()
                    crew = cargar_agente()
                    resultado = crew.kickoff(inputs={"pregunta": pregunta_usuario})
                    end_time = time.time()
                    tiempo_ejecucion = round(end_time - start_time, 2)
                    
                    st.success("✅ ¡Análisis completado!")
                    st.markdown("---")
                    
                    # Layout de dos columnas para el resultado
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(resultado.raw)
                        
                    with col2:
                        st.metric(label="⏱️ Tiempo de respuesta", value=f"{tiempo_ejecucion} s")
                        st.metric(label="📊 Estado", value="Exitoso")
                        st.caption("Modelo: Qwen 2.5 7B (Local)")
                    
                except Exception as e:
                    st.error(f"❌ Ocurrió un error: {str(e)}")
                    st.info("💡 **Tip:** Asegúrate de que Ollama esté corriendo (`ollama serve`) y de que el modelo `qwen2.5:7b` esté descargado.")