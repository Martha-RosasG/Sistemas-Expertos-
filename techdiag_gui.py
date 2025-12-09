# techdiag_gui.py
# Interfaz gráfica y motor de inferencia por porcentaje de coincidencia para TechDiag.

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "techdiag.db"

class TechDiagApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechDiag — Diagnóstico de Computadoras")
        self.root.geometry("760x560")
        self.root.configure(bg="#1e1e2f")  # fondo oscuro

        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la base de datos: {e}")
            root.destroy()
            return

        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        self.limpiar()
        header = tk.Label(self.root, text="TechDiag", font=("Segoe UI", 26, "bold"), bg="#1e1e2f", fg="#e6e6e6")
        header.pack(pady=(20, 5))

        sub = tk.Label(self.root, text="Seleccione el sistema a evaluar", font=("Segoe UI", 12), bg="#1e1e2f", fg="#cfcfcf")
        sub.pack(pady=(0, 15))

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack()

        sistemas = self.obtener_sistemas()
        for sid, nombre in sistemas:
            btn = tk.Button(frame, text=nombre, width=18, height=2,
                            command=lambda s_id=sid, s_nombre=nombre: self.cargar_sintomas(s_id, s_nombre),
                            bg="#2b2b45", fg="#ffffff", bd=0, font=("Segoe UI", 11, "bold"))
            btn.pack(side="left", padx=12)

    def obtener_sistemas(self):
        self.cur.execute("SELECT id, nombre FROM sistemas")
        return self.cur.fetchall()

    def cargar_sintomas(self, sistema_id, sistema_nombre):
        self.limpiar()
        self.sistema_id = sistema_id
        title = tk.Label(self.root, text=f"Sistema: {sistema_nombre}", font=("Segoe UI", 18, "bold"), bg="#1e1e2f", fg="#ffffff")
        title.pack(pady=12)
        # Obtener síntomas relacionados con ese sistema (distinct)
        query = """
            SELECT DISTINCT s.id, s.descripcion
            FROM sintomas s
            JOIN relacion r ON s.id = r.sintoma_id
            JOIN fallas f ON r.falla_id = f.id
            WHERE f.sistema_id = ?
            ORDER BY s.descripcion
        """
        self.cur.execute(query, (sistema_id,))
        sintomas = self.cur.fetchall()

        if not sintomas:
            tk.Label(self.root, text="No hay síntomas registrados para este sistema.", bg="#1e1e2f", fg="#ff6b6b").pack()
            tk.Button(self.root, text="Volver", command=self.crear_pantalla_inicio, bg="#34495e", fg="white").pack(pady=10)
            return

        # Scrollable frame
        container = tk.Frame(self.root, bg="#2b2b45", bd=1)
        container.pack(padx=18, pady=10, fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#2b2b45", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#2b2b45")
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Checkboxes
        self.chk_vars = []
        self.chk_meta = []  # (sintoma_id, descripcion)
        for sid, desc in sintomas:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.scroll_frame, text=desc, variable=var,
                                 font=("Segoe UI", 11), bg="#2b2b45", fg="#e6e6e6",
                                 activebackground="#2b2b45", selectcolor="#44475a")
            chk.pack(anchor="w", padx=12, pady=6)
            self.chk_vars.append(var)
            self.chk_meta.append((sid, desc))

        # Acción
        action_frame = tk.Frame(self.root, bg="#1e1e2f")
        action_frame.pack(pady=12)
        tk.Button(action_frame, text="Cancelar", command=self.crear_pantalla_inicio, bg="#7f8c8d", fg="white").pack(side="left", padx=8)
        tk.Button(action_frame, text="Diagnosticar", command=self.ejecutar_inferencia, bg="#2ecc71", fg="black", font=("Segoe UI", 11, "bold")).pack(side="left", padx=8)

    def ejecutar_inferencia(self):
        seleccionados = [self.chk_meta[i] for i, v in enumerate(self.chk_vars) if v.get() == 1]
        if not seleccionados:
            messagebox.showwarning("Falta seleccionar", "Seleccione al menos un síntoma para diagnosticar.")
            return

        # Convertir a lista de ids
        ids_seleccionados = [sid for sid, _ in seleccionados]

        # 1) obtener todas las fallas del sistema
        self.cur.execute("SELECT id, nombre, solucion FROM fallas WHERE sistema_id = ?", (self.sistema_id,))
        fallas = self.cur.fetchall()

        resultados = []
        for falla_id, nombre, solucion in fallas:
            # obtener todos los sintoma_ids asociados a esta falla
            self.cur.execute("SELECT sintoma_id FROM relacion WHERE falla_id = ?", (falla_id,))
            sint_ids = [row[0] for row in self.cur.fetchall()]
            if not sint_ids:
                continue
            # contar coincidencias
            coincidencias = sum(1 for s in ids_seleccionados if s in sint_ids)
            certeza = coincidencias / len(sint_ids)  # porcentaje de coincidencia (0..1)
            resultados.append((nombre, solucion, certeza, coincidencias, len(sint_ids)))

        # ordenar por certeza descendente, luego por coincidencias
        resultados.sort(key=lambda x: (x[2], x[3]), reverse=True)

        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        self.limpiar()
        tk.Label(self.root, text="Resultados", font=("Segoe UI", 20, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=10)

        if not resultados:
            tk.Label(self.root, text="No se encontró coincidencia significativa.", bg="#1e1e2f", fg="#ff6b6b").pack(pady=12)
            tk.Button(self.root, text="Volver", command=self.crear_pantalla_inicio, bg="#34495e", fg="white").pack(pady=10)
            return

        # Mostrar top 3
        top = resultados[:3]
        for nombre, solucion, certeza, coincidencias, total_sint in top:
            porcentaje = f"{certeza*100:.0f}%"
            card = tk.Frame(self.root, bg="#2b2b45", bd=1, relief="solid")
            card.pack(fill="x", padx=18, pady=8)
            tk.Label(card, text=nombre, font=("Segoe UI", 14, "bold"), bg="#2b2b45", fg="#ffd166").pack(anchor="w", padx=12, pady=(8,0))
            tk.Label(card, text=f"Probabilidad: {porcentaje} ({coincidencias}/{total_sint} síntomas coinciden)", bg="#2b2b45", fg="#e6e6e6", font=("Segoe UI", 10)).pack(anchor="w", padx=12)
            tk.Label(card, text="Recomendación:", bg="#2b2b45", fg="#cfcfcf", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(6,0))
            tk.Label(card, text=solucion, bg="#2b2b45", fg="#e6e6e6", wraplength=700, justify="left").pack(anchor="w", padx=12, pady=(0,8))

        # Consejos
        tk.Label(self.root, text="Consejo: si la probabilidad es baja (<40%), recolecte más síntomas o realice pruebas técnicas (memtest, CHKDSK, etc.).",
                 bg="#1e1e2f", fg="#9aa0b4", font=("Segoe UI", 9)).pack(pady=(10,6))

        btns = tk.Frame(self.root, bg="#1e1e2f")
        btns.pack(pady=10)
        tk.Button(btns, text="Nuevo diagnóstico", command=self.crear_pantalla_inicio, bg="#3498db", fg="white").pack(side="left", padx=8)
        tk.Button(btns, text="Salir", command=self.root.quit, bg="#7f8c8d", fg="white").pack(side="left", padx=8)

    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TechDiagApp(root)
    root.mainloop()