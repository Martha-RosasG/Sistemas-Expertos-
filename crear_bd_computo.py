# crear_bd_computo.py
# Crea la base de datos 'techdiag.db' para TechDiag (Sistema experto diagnóstico de computadoras).

import sqlite3
import os

DB_NAME = "techdiag.db"

def crear_bd():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Tablas: sistemas, fallas, sintomas, relacion
    cur.execute("""
    CREATE TABLE sistemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE fallas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sistema_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        solucion TEXT,
        FOREIGN KEY(sistema_id) REFERENCES sistemas(id)
    )
    """)

    cur.execute("""
    CREATE TABLE sintomas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE relacion (
        falla_id INTEGER,
        sintoma_id INTEGER,
        importancia INTEGER DEFAULT 1, -- 1: baja, 2: media, 3: alta (para futura ampliación)
        FOREIGN KEY(falla_id) REFERENCES fallas(id),
        FOREIGN KEY(sintoma_id) REFERENCES sintomas(id)
    )
    """)

    # Insertar sistemas
    sistemas = [("Hardware",), ("Software",), ("Red",)]
    cur.executemany("INSERT INTO sistemas(nombre) VALUES (?)", sistemas)

    # Insertar fallas (con sistema_id)
    # Obtenemos ids de sistemas
    cur.execute("SELECT id, nombre FROM sistemas")
    sids = {row[1]: row[0] for row in cur.fetchall()}

    fallas = [
        (sids["Hardware"], "RAM defectuosa", "Reemplazar módulos de RAM o ejecutar memtest."),
        (sids["Hardware"], "Disco con sectores dañados", "Respaldar datos y ejecutar CHKDSK; considerar cambio de disco."),
        (sids["Hardware"], "Sobrecalentamiento CPU/GPU", "Limpiar ventiladores, revisar pasta térmica y flujo de aire."),
        (sids["Hardware"], "Fuente de poder inestable", "Medir voltajes; reemplazar fuente si hay fluctuaciones."),
        (sids["Software"], "Sistema operativo corrupto", "Reparar arranque o reinstalar sistema operativo tras respaldos."),
        (sids["Software"], "Malware/virus", "Escaneo con antivirus offline y limpieza; reinstalación si es necesario."),
        (sids["Software"], "Drivers desactualizados", "Actualizar drivers desde sitio oficial del fabricante."),
        (sids["Software"], "Programa conflictivo", "Identificar programa y desinstalar/actualizar."),
        (sids["Red"], "Router mal configurado", "Revisar configuración: NAT, DHCP y reiniciar router."),
        (sids["Red"], "Interferencia WiFi", "Cambiar canal, mover router o usar banda 5GHz si es posible."),
        (sids["Red"], "DNS incorrecto/caído", "Configurar DNS público (ej. 1.1.1.1/8.8.8.8) o contactar ISP."),
        (sids["Red"], "Adaptador de red dañado", "Probar con adaptador USB/Ethernet distinto o reinstalar controlador.")
    ]
    cur.executemany("INSERT INTO fallas(sistema_id, nombre, solucion) VALUES (?,?,?)", fallas)

    # Insertar síntomas (únicos)
    sintomas_list = [
        "Pantalla azul (BSOD)",
        "Reinicios aleatorios",
        "Rendimiento muy lento",
        "Ruidos extraños en disco",
        "Archivos corruptos o faltantes",
        "Ventiladores a máxima velocidad constantemente",
        "Apagados súbitos durante juegos",
        "Errores de inicio del sistema",
        "Pop-ups sospechosos",
        "Programas que no abren",
        "Conexión a internet intermitente",
        "Alta latencia (lag) en juegos/streaming",
        "Se desconecta solo del WiFi",
        "Otros dispositivos sí tienen Internet",
        "Error DNS en navegador",
        "Controladores reportan fallos",
        "Actualización del sistema falla repetidamente",
        "Luz de actividad del disco siempre encendida"
    ]
    cur.executemany("INSERT INTO sintomas(descripcion) VALUES (?)", [(s,) for s in sintomas_list])

    # Construir relaciones (falla_id, sintoma_id, importancia)
    # Obtener mapping sintoma -> id
    cur.execute("SELECT id, descripcion FROM sintomas")
    sin_map = {row[1]: row[0] for row in cur.fetchall()}

    # Obtener mapping falla -> id
    cur.execute("SELECT id, nombre FROM fallas")
    falla_map = {row[1]: row[0] for row in cur.fetchall()}

    relaciones = [
        # RAM defectuosa
        (falla_map["RAM defectuosa"], sin_map["Pantalla azul (BSOD)"], 3),
        (falla_map["RAM defectuosa"], sin_map["Reinicios aleatorios"], 3),
        (falla_map["RAM defectuosa"], sin_map["Errores de inicio del sistema"], 2),
        (falla_map["RAM defectuosa"], sin_map["Archivos corruptos o faltantes"], 2),

        # Disco con sectores dañados
        (falla_map["Disco con sectores dañados"], sin_map["Ruidos extraños en disco"], 3),
        (falla_map["Disco con sectores dañados"], sin_map["Archivos corruptos o faltantes"], 3),
        (falla_map["Disco con sectores dañados"], sin_map["Luz de actividad del disco siempre encendida"], 2),

        # Sobrecalentamiento
        (falla_map["Sobrecalentamiento CPU/GPU"], sin_map["Ventiladores a máxima velocidad constantemente"], 3),
        (falla_map["Sobrecalentamiento CPU/GPU"], sin_map["Apagados súbitos durante juegos"], 3),
        (falla_map["Sobrecalentamiento CPU/GPU"], sin_map["Rendimiento muy lento"], 2),

        # Fuente inestable
        (falla_map["Fuente de poder inestable"], sin_map["Reinicios aleatorios"], 3),
        (falla_map["Fuente de poder inestable"], sin_map["Apagados súbitos durante juegos"], 2),

        # Sistema operativo corrupto
        (falla_map["Sistema operativo corrupto"], sin_map["Errores de inicio del sistema"], 3),
        (falla_map["Sistema operativo corrupto"], sin_map["Actualización del sistema falla repetidamente"], 2),
        (falla_map["Sistema operativo corrupto"], sin_map["Programas que no abren"], 2),

        # Malware / virus
        (falla_map["Malware/virus"], sin_map["Pop-ups sospechosos"], 3),
        (falla_map["Malware/virus"], sin_map["Rendimiento muy lento"], 2),
        (falla_map["Malware/virus"], sin_map["Archivos corruptos o faltantes"], 1),

        # Drivers desactualizados
        (falla_map["Drivers desactualizados"], sin_map["Controladores reportan fallos"], 3),
        (falla_map["Drivers desactualizados"], sin_map["Programas que no abren"], 2),

        # Programa conflictivo
        (falla_map["Programa conflictivo"], sin_map["Programas que no abren"], 3),
        (falla_map["Programa conflictivo"], sin_map["Rendimiento muy lento"], 1),

        # Router mal configurado
        (falla_map["Router mal configurado"], sin_map["Conexión a internet intermitente"], 3),
        (falla_map["Router mal configurado"], sin_map["Otros dispositivos sí tienen Internet"], 2),

        # Interferencia WiFi
        (falla_map["Interferencia WiFi"], sin_map["Se desconecta solo del WiFi"], 3),
        (falla_map["Interferencia WiFi"], sin_map["Alta latencia (lag) en juegos/streaming"], 2),

        # DNS incorrecto/caído
        (falla_map["DNS incorrecto/caído"], sin_map["Error DNS en navegador"], 3),

        # Adaptador de red dañado
        (falla_map["Adaptador de red dañado"], sin_map["Conexión a internet intermitente"], 3),
        (falla_map["Adaptador de red dañado"], sin_map["Otros dispositivos sí tienen Internet"], 3)
    ]

    cur.executemany("INSERT INTO relacion(falla_id, sintoma_id, importancia) VALUES (?,?,?)", relaciones)

    conn.commit()
    conn.close()
    print(f"Base de datos '{DB_NAME}' creada y poblada correctamente.")

if __name__ == "__main__":
    crear_bd()