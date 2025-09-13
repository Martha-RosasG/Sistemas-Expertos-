#Practica_2_Sistemas_expertos
# chat_sencillo.py
import json
import os
import difflib

# Archivo donde guardaremos el conocimiento
ARCHIVO_BASE = "base_conocimiento.json"

# Función para cargar la base de conocimiento
def cargar_base():
    if os.path.exists(ARCHIVO_BASE):
        with open(ARCHIVO_BASE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Base precargada
        return {
            "Hola": "¡Hola! ¿Cómo estás?",
            "¿Cómo estás?": "Estoy bien, gracias. ¿Y tú?",
            "¿De qué te gustaría hablar?": "Podemos hablar de tecnología, hobbies o cualquier tema que te interese."
        }

# Función para guardar la base de conocimiento
def guardar_base(base):
    with open(ARCHIVO_BASE, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4, ensure_ascii=False)

# Función para buscar la respuesta más cercana
def buscar_respuesta(base, mensaje):
    llaves = list(base.keys())
    coincidencias = difflib.get_close_matches(mensaje, llaves, n=1, cutoff=0.6)
    if coincidencias:
        return base[coincidencias[0]]
    else:
        return None

# Función principal del chat
def chat():
    base = cargar_base()
    print("Chat iniciado. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tú: ").strip()
        if mensaje.lower() == "salir":
            print("Chat finalizado.")
            break

        respuesta = buscar_respuesta(base, mensaje)
        if respuesta:
            print(f"Bot: {respuesta}")
        else:
            # Preguntar al usuario cómo debería responder
            nueva_respuesta = input("No conozco la respuesta. ¿Qué debería decir? ").strip()
            base[mensaje] = nueva_respuesta
            guardar_base(base)
            print("Bot: Gracias, he aprendido algo nuevo.")

# Ejecutar chat
if __name__ == "__main__":
    chat()
