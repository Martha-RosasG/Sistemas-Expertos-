import json
import os
import math

# Nombre del archivo para la base de conocimiento de perros
DB_FILE = "razas_perros.json"

def cargar_base_de_datos():
    """Carga la base de datos de razas desde el archivo JSON."""
    if not os.path.exists(DB_FILE):
        # Si el archivo no existe, crea una base de datos inicial con algunas razas.
        print("Creando una nueva base de conocimiento de razas de perros...")
        return {
            "razas": [
                {
                    "nombre": "Golden Retriever",
                    "atributos": {
                        "es_de_tamano_grande": "si",
                        "tiene_pelo_largo": "si",
                        "es_considerado_un_perro_de_trabajo": "si",
                        "es_ideal_para_apartamentos": "no",
                        "es_hipoalergenico": "no"
                    }
                },
                {
                    "nombre": "Chihuahua",
                    "atributos": {
                        "es_de_tamano_grande": "no",
                        "tiene_pelo_largo": "no",
                        "es_considerado_un_perro_de_trabajo": "no",
                        "es_ideal_para_apartamentos": "si",
                        "es_hipoalergenico": "no"
                    }
                },
                {
                    "nombre": "Pastor Alemán",
                    "atributos": {
                        "es_de_tamano_grande": "si",
                        "tiene_pelo_largo": "no",
                        "es_considerado_un_perro_de_trabajo": "si",
                        "es_ideal_para_apartamentos": "no",
                        "es_hipoalergenico": "no"
                    }
                },
                {
                    "nombre": "Poodle (Caniche)",
                    "atributos": {
                        "es_de_tamano_grande": "no", # Refiriéndose al estándar más pequeño
                        "tiene_pelo_largo": "si", # Pelo rizado que crece
                        "es_considerado_un_perro_de_trabajo": "si",
                        "es_ideal_para_apartamentos": "si",
                        "es_hipoalergenico": "si"
                    }
                }
            ]
        }
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_base_de_datos(db):
    """Guarda la base de datos de razas en el archivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def obtener_respuesta_valida(pregunta):
    """Pide al usuario una respuesta 'si' o 'no' y la valida."""
    while True:
        respuesta = input(f"{pregunta} (si/no): ").lower().strip()
        if respuesta in ["si", "s", "yes", "y"]:
            return "si"
        if respuesta in ["no", "n"]:
            return "no"
        print("Respuesta no válida. Por favor, responde 'si' o 'no'.")

def encontrar_mejor_pregunta(posibles_razas, preguntas_hechas):
    """Encuentra la pregunta que mejor divide la lista de razas restantes."""
    mejor_pregunta = None
    menor_diferencia = float('inf')

    preguntas_posibles = set()
    for raza in posibles_razas:
        preguntas_posibles.update(raza["atributos"].keys())

    preguntas_a_evaluar = list(preguntas_posibles - set(preguntas_hechas))

    if not preguntas_a_evaluar:
        return None

    for pregunta in preguntas_a_evaluar:
        conteo_si = 0
        conteo_no = 0
        for raza in posibles_razas:
            if raza["atributos"].get(pregunta) == "si":
                conteo_si += 1
            else:
                conteo_no += 1
        
        if conteo_si == 0 or conteo_no == 0:
            continue

        diferencia = abs(conteo_si - conteo_no)
        if diferencia < menor_diferencia:
            menor_diferencia = diferencia
            mejor_pregunta = pregunta

    return mejor_pregunta

def modulo_aprendizaje(db, respuestas_usuario, raza_incorrecta):
    """Inicia el proceso de aprendizaje cuando el sistema falla."""
    print("\n¡Vaya! Me he rendido. Ayúdame a aprender.")
    nombre_correcto = input("¿En qué raza de perro estabas pensando? ").strip().title()

    raza_existente = next((r for r in db["razas"] if r["nombre"].lower() == nombre_correcto.lower()), None)

    if raza_existente and raza_existente["nombre"] == raza_incorrecta:
        print("¡Oh! Parece que hubo una contradicción en tus respuestas.")
        return

    pregunta_nueva = input(f"Dame una pregunta que se responda con 'sí' para un {nombre_correcto}, pero con 'no' para un {raza_incorrecta}: ").strip()
    
    if not pregunta_nueva.endswith('?'):
        pregunta_nueva += '?'

    clave_pregunta = pregunta_nueva.lower().replace("¿", "").replace("?", "").replace(" ", "_")

    if not raza_existente:
        nueva_raza = {
            "nombre": nombre_correcto,
            "atributos": respuestas_usuario
        }
        nueva_raza["atributos"][clave_pregunta] = "si"
        db["razas"].append(nueva_raza)
        print(f"He aprendido sobre la raza {nombre_correcto}.")
    else:
        raza_existente["atributos"][clave_pregunta] = "si"
        print(f"He actualizado mi conocimiento sobre la raza {nombre_correcto}.")

    if raza_incorrecta:
        raza_a_actualizar = next((r for r in db["razas"] if r["nombre"] == raza_incorrecta), None)
        if raza_a_actualizar:
            raza_a_actualizar["atributos"][clave_pregunta] = "no"

    guardar_base_de_datos(db)
    print("¡Gracias! Mi conocimiento ha sido actualizado. ✨")

def jugar():
    """Función principal que ejecuta el bucle del juego."""
    db = cargar_base_de_datos()
    posibles_razas = list(db["razas"])
    preguntas_hechas = []
    respuestas_usuario = {}

    print("\n--- ¡Adivina la Raza de Perro! ---")
    print("Piensa en una raza de perro y yo intentaré adivinarla. Responde con 'si' o 'no'.")
    
    while len(posibles_razas) > 1:
        pregunta = encontrar_mejor_pregunta(posibles_razas, preguntas_hechas)

        if pregunta is None:
            break
            
        pregunta_formateada = f"¿La raza de tu perro {pregunta.replace('_', ' ')}?"
        respuesta = obtener_respuesta_valida(pregunta_formateada)

        respuestas_usuario[pregunta] = respuesta
        preguntas_hechas.append(pregunta)

        posibles_razas = [
            r for r in posibles_razas if r["atributos"].get(pregunta, "no") == respuesta
        ]

    if len(posibles_razas) == 1:
        raza_adivinada = posibles_razas[0]
        respuesta_final = obtener_respuesta_valida(f"La raza que tienes en mente es... ¿un {raza_adivinada['nombre']}?")
        if respuesta_final == "si":
            print(f"\n¡Genial! ¡He adivinado! Era un {raza_adivinada['nombre']}. 🎉")
        else:
            modulo_aprendizaje(db, respuestas_usuario, raza_adivinada['nombre'])

    elif len(posibles_razas) == 0:
        print("\n🤔 No conozco ninguna raza con esas características.")
        modulo_aprendizaje(db, respuestas_usuario, None)
    
    else:
        print("\nNo tengo suficientes preguntas para diferenciar a las razas restantes.")
        print("Posibles razas:", ", ".join([r['nombre'] for r in posibles_razas]))
        modulo_aprendizaje(db, respuestas_usuario, posibles_razas[0]['nombre'])


if __name__ == "__main__":
    while True:
        jugar()
        if obtener_respuesta_valida("\n¿Quieres jugar otra vez?") == "no":
            print("¡Gracias por jugar!")
            break