# crear_bd.py
import sqlite3

# Conectar (crea el archivo si no existe)
conn = sqlite3.connect("ventas.db")
cursor = conn.cursor()

# Crear tabla de ventas
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    producto TEXT,
    categoria TEXT,
    unidades INTEGER,
    precio_unitario REAL,
    total REAL
)
""")

# Insertar datos de ejemplo (los mismos del CSV)
datos = [
    ("2026-01-05", "Laptop Pro X", "Tecnología", 15, 1200, 18000),
    ("2026-01-12", "Mouse Inalámbrico", "Accesorios", 50, 25, 1250),
    ("2026-01-18", "Monitor 27", "Tecnología", 10, 300, 3000),
    ("2026-02-03", "Laptop Pro X", "Tecnología", 8, 1200, 9600),
    ("2026-02-15", "Teclado Mecánico", "Accesorios", 30, 80, 2400),
    ("2026-02-28", "Monitor 27", "Tecnología", 12, 300, 3600),
    ("2026-03-10", "Laptop Pro X", "Tecnología", 20, 1200, 24000),
    ("2026-03-15", "Mouse Inalámbrico", "Accesorios", 40, 25, 1000),
    ("2026-03-22", "Silla Ergonómica", "Mobiliario", 5, 250, 1250),
    ("2026-03-28", "Teclado Mecánico", "Accesorios", 25, 80, 2000),
]

cursor.executemany("""
INSERT INTO ventas (fecha, producto, categoria, unidades, precio_unitario, total)
VALUES (?, ?, ?, ?, ?, ?)
""", datos)

conn.commit()
conn.close()

print("✅ Base de datos 'ventas.db' creada exitosamente con 10 registros.")