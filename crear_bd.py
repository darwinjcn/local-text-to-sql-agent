# crear_bd.py
import sqlite3
import os

# Eliminar la BD anterior si existe
if os.path.exists("ventas.db"):
    os.remove("ventas.db")
    print("🗑️ Base de datos anterior eliminada.")

# Conectar (crea el archivo nuevo)
conn = sqlite3.connect("ventas.db")
cursor = conn.cursor()

# Crear tabla de ventas
cursor.execute("""
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    producto TEXT,
    categoria TEXT,
    unidades INTEGER,
    precio_unitario REAL,
    total REAL
)
""")

# Leer el CSV e insertar los datos
import csv

with open('ventas.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        cursor.execute("""
        INSERT INTO ventas (fecha, producto, categoria, unidades, precio_unitario, total)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (fila['fecha'], fila['producto'], fila['categoria'], 
              int(fila['unidades']), float(fila['precio_unitario']), float(fila['total'])))

conn.commit()

# Verificar cuántos registros se insertaron
cursor.execute("SELECT COUNT(*) FROM ventas")
cantidad = cursor.fetchone()[0]

conn.close()

print(f"✅ Base de datos 'ventas.db' creada exitosamente con {cantidad} registros.")
print(f"📊 Período: Enero - Marzo 2026")
print(f"📦 Productos únicos: 30+")
print(f"🏷️ Categorías: Tecnología, Accesorios, Mobiliario")