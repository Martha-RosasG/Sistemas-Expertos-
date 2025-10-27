# Misterio en el Castillo: El Señor de los Anillos 


import random
import os

# -------------------------------------------------------
# 1 Datos del juego
# -------------------------------------------------------

SUSPECTOS = [
    "Aragorn, el caballero real",
    "Arwen, la condesa",
    "Maestro Legolas, el alquimista",
    "Monje Sam, el bibliotecario",
    "Don Frodo, el capitán de la guardia"
]

LUGARES = [
    "Gran Salón",
    "Torre del Hechicero",
    "Mazmorras",
    "Jardín Interior",
    "Armería"
]

OBJETOS = [
    "Espada Antigua",
    "Frasco de Veneno",
    "Candelabro de Hierro",
    "Ballesta Real",
    "Libro Encantado"
]

CASOS = [
    {
        "asesino": "Arwen, la condesa",
        "arma": "Candelabro de Hierro",
        "sitio": "Gran Salón",
        "relato": "¡Correcto! La condesa Arwen descubrió que el rey planeaba desterrarla. Durante el banquete en el Gran Salón, usó el Candelabro de Hierro para cumplir su venganza."
    },
    {
        "asesino": "Maestro Legolas, el alquimista",
        "arma": "Frasco de Veneno",
        "sitio": "Torre del Hechicero",
        "relato": "¡Has resuelto el misterio! El Maestro Legolas temía que su secreto sobre la Piedra Filosofal fuera revelado. En su Torre del Hechicero, vertió un Frasco de Veneno en la copa de su aprendiz."
    },
    {
        "asesino": "Aragorn, el caballero real",
        "arma": "Espada Antigua",
        "sitio": "Armería",
        "relato": "¡Excelente deducción! Aragorn juró proteger el reino, pero su ambición lo cegó. En la Armería, usó la Espada Antigua para eliminar al consejero que sabía demasiado."
    },
    {
        "asesino": "Monje Sam, el bibliotecario",
        "arma": "Libro Encantado",
        "sitio": "Mazmorras",
        "relato": "¡Misterio resuelto! El Monje Sam descubrió un grimorio prohibido. En las frías Mazmorras, liberó un hechizo oscuro del Libro Encantado contra su rival."
    },
    {
        "asesino": "Don Frodo, el capitán de la guardia",
        "arma": "Ballesta Real",
        "sitio": "Jardín Interior",
        "relato": "¡Lo has logrado! Durante una noche silenciosa en el Jardín Interior, Don Frodo usó la Ballesta Real para eliminar al espía que traicionó al castillo."
    }
]

# -------------------------------------------------------
# 2 Funciones auxiliares
# -------------------------------------------------------

def limpiar():
    """Limpia la consola según el sistema operativo."""
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)

def mostrar_listas():
    """Despliega las listas de opciones disponibles."""
    print("\n SOSPECHOSOS ")
    for i, nombre in enumerate(SUSPECTOS, 1):
        print(f"[{i}] {nombre}")

    print("\n ARMAS ")
    for i, objeto in enumerate(OBJETOS, 1):
        print(f"[{i}] {objeto}")

    print("\n LOCACIONES ")
    for i, sitio in enumerate(LUGARES, 1):
        print(f"[{i}] {sitio}")

def elegir_opcion(lista, tipo):
    """Permite elegir un elemento de una lista mediante su número."""
    while True:
        try:
            seleccion = int(input(f"\nSelecciona el número del {tipo}: "))
            if 1 <= seleccion <= len(lista):
                return lista[seleccion - 1]
            else:
                print("Número inválido, intenta nuevamente.")
        except ValueError:
            print("Debes escribir un número válido.")

# -------------------------------------------------------
# 3 Lógica del juego
# -------------------------------------------------------

def iniciar_juego():
    limpiar()
    print("*" * 60)
    print(" BIENVENIDO A: CLUE — EL MISTERIO EN EL CASTILLO ")
    print("Un crimen ha ocurrido en las murallas del reino...")
    print("Tu objetivo: descubrir al culpable, el arma usada y el lugar del hecho.")
    print("*" * 60)

    caso_real = random.choice(CASOS)
    turno = 0

    while True:
        turno += 1
        print(f"\n--- INTENTO #{turno} ---")
        mostrar_listas()

        print("\n HAZ TU ACUSACIÓN ")
        sospechoso = elegir_opcion(SUSPECTOS, "sospechoso")
        arma = elegir_opcion(OBJETOS, "arma")
        lugar = elegir_opcion(LUGARES, "locación")

        limpiar()
        print(f"\nTu acusación: {sospechoso} con el/la {arma} en el/la {lugar}.")

        if (sospechoso == caso_real["asesino"] and
            arma == caso_real["arma"] and
            lugar == caso_real["sitio"]):
            
            print("\n" + "*" * 60)
            print(" ¡HAS DESCUBIERTO LA VERDAD! ")
            print(caso_real["relato"])
            print("*" * 60)
            break
        else:
            aciertos = sum([
                sospechoso == caso_real["asesino"],
                arma == caso_real["arma"],
                lugar == caso_real["sitio"]
            ])
            print("\n Tu acusación es incorrecta...")
            print(f" PISTA: Acertaste {aciertos} elemento(s) de la combinación.")
            print("Investiga más y vuelve a intentarlo.")
            input("\nPresiona Enter para continuar...")
            limpiar()

# -------------------------------------------------------
# 4. Ejecución principal
# -------------------------------------------------------

if __name__ == "__main__":
    iniciar_juego()
