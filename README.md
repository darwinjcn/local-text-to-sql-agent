# 🤖 Mi Primer Agente de IA

Proyecto profesional para construir agentes de IA autónomos usando herramientas **100% gratuitas, locales y open-source**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Agents-orange?logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?logo=linux)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Objetivos del Proyecto

- Implementar orquestación de agentes multi-rol con **CrewAI**.
- Ejecutar modelos de lenguaje (LLMs) de forma local y privada con **Ollama**.
- Conectar agentes con datos reales (archivos CSV y bases de datos SQL).
- Aplicar el **Patrón Híbrido**: Python para cálculos deterministas, LLM para redacción y razonamiento.

## 🧠 Arquitectura del Agente

```mermaid
flowchart LR
    U(["👤 Usuario"]) -->|"Pregunta en lenguaje natural"| A["🤖 Agente CrewAI"]
    A -->|"Genera SQL"| T["🔧 Herramienta SQL"]
    T --> BD[("🗄️ SQLite")]
    BD -->|"Resultados exactos"| A
    A -->|"Contexto + datos"| L["🧠 Qwen 2.5 7B (Ollama)"]
    L -->|"Respuesta redactada"| U
```

> El agente nunca inventa datos: el cálculo lo hace SQLite/Pandas y el LLM solo interpreta y redacta.

## 📷 Demo

Salida de la ejecución del agente Text-to-SQL (`python agente_sql.py`):

![Agente Text-to-SQL en acción](assets/demo_sql.png)

## 🛠️ Stack Tecnológico


| Tecnología                 | Rol en el proyecto                   |
| -------------------------- | ------------------------------------ |
| **Python 3.x**             | Lenguaje principal del proyecto      |
| **CrewAI**                 | Framework de orquestación de agentes |
| **Ollama + Qwen 2.5 (7B)** | Motor de inferencia local y privado  |
| **Pandas**                 | Manipulación y análisis de datos     |
| **SQLite**                 | Base de datos relacional local       |


## 📂 Estructura del Proyecto

```text
mi-primer-agente/
├── test_conexion.py              # Prueba de conexión con el LLM local
├── agente_herramienta_custom.py  # Creación de herramientas personalizadas (@tool)
├── agente_csv_hibrido.py         # Patrón híbrido: Pandas calcula, LLM redacta
├── agente_sql.py                 # Agente Text-to-SQL autónomo
├── crear_bd.py                   # Script para generar la BD SQLite de prueba
└── ventas.csv                    # Dataset de ejemplo
```

## 🚀 Cómo Ejecutar

### 1. Requisitos previos

Tener [Ollama](https://ollama.com) instalado y descargar el modelo:

```bash
ollama pull qwen2.5:7b
```

### 2. Instalación del entorno

```bash
pip install crewai crewai-tools langchain-community pandas tabulate
```

### 3. Verificar la conexión con el LLM local

```bash
python test_conexion.py
```

### 4. Generar la base de datos de prueba

```bash
python crear_bd.py
```

### 5. Ejecutar los agentes

```bash
# Agente con herramientas personalizadas
python agente_herramienta_custom.py

# Agente híbrido (Pandas calcula, LLM redacta)
python agente_csv_hibrido.py

# Agente Text-to-SQL autónomo
python agente_sql.py
```

## 💡 Aprendizajes Clave

1. **Limitaciones del Tool Calling:** los modelos pequeños (&lt;7B) tienden a alucinar al intentar generar código SQL o llamar a funciones complejas.
2. **Arquitectura Híbrida:** delegar el cálculo a Python (Pandas/SQL) y la redacción al LLM garantiza cero alucinaciones y 100% de precisión en los datos.
3. **Privacidad total:** al ejecutar el LLM localmente con Ollama, ningún dato sale de tu máquina.
4. **Modularidad:** separar la conexión (`test_conexion.py`), las herramientas (`@tool`) y los agentes hace el proyecto fácil de extender.

---

## 🔮 Próximos Pasos (Roadmap)

- [ ] Integrar interfaz web con Streamlit para usuarios no técnicos.
- [ ] Conectar el agente a una base de datos PostgreSQL en la nube.
- [ ] Implementar un sistema Multi-Agente (Data Engineer + Business Analyst).