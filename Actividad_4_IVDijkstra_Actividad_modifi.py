#Actividad_4_IVDijkstra_Actividad_modificada
import numpy as np

# Matriz de adyacencia: distancias en km entre colonias
matriz_adyacente = {
    'ColoniaA': {'ColoniaA': 0, 'ColoniaB': 2, 'ColoniaC': 0, 'ColoniaD': 0, 'ColoniaE': 0, 'ColoniaF': 1, 'ColoniaG': 0, 'Destino': 0},
    'ColoniaB': {'ColoniaA': 2, 'ColoniaB': 0, 'ColoniaC': 2, 'ColoniaD': 2, 'ColoniaE': 0, 'ColoniaF': 0, 'ColoniaG': 0, 'Destino': 0},
    'ColoniaC': {'ColoniaA': 0, 'ColoniaB': 2, 'ColoniaC': 0, 'ColoniaD': 0, 'ColoniaE': 3, 'ColoniaF': 0, 'ColoniaG': 0, 'Destino': 1},
    'ColoniaD': {'ColoniaA': 0, 'ColoniaB': 2, 'ColoniaC': 0, 'ColoniaD': 0, 'ColoniaE': 4, 'ColoniaF': 3, 'ColoniaG': 0, 'Destino': 0},
    'ColoniaE': {'ColoniaA': 0, 'ColoniaB': 0, 'ColoniaC': 3, 'ColoniaD': 4, 'ColoniaE': 0, 'ColoniaF': 0, 'ColoniaG': 7, 'Destino': 0},
    'ColoniaF': {'ColoniaA': 1, 'ColoniaB': 0, 'ColoniaC': 0, 'ColoniaD': 3, 'ColoniaE': 0, 'ColoniaF': 0, 'ColoniaG': 5, 'Destino': 0},
    'ColoniaG': {'ColoniaA': 0, 'ColoniaB': 0, 'ColoniaC': 0, 'ColoniaD': 0, 'ColoniaE': 7, 'ColoniaF': 5, 'ColoniaG': 0, 'Destino': 6},
    'Destino':  {'ColoniaA': 0, 'ColoniaB': 0, 'ColoniaC': 1, 'ColoniaD': 0, 'ColoniaE': 0, 'ColoniaF': 0, 'ColoniaG': 6, 'Destino': 0}
}

def encontrar_camino_mas_corto(grafo, inicio):
    nodos = list(grafo.keys())
    distancias = {nodo: np.inf for nodo in nodos}
    distancias[inicio] = 0
    conjunto_visitado = set()
    rutas = {nodo: None for nodo in nodos}

    while len(conjunto_visitado) < len(nodos):
        nodo_actual = None
        for nodo in nodos:
            if nodo not in conjunto_visitado:
                if nodo_actual is None or distancias[nodo] < distancias[nodo_actual]:
                    nodo_actual = nodo

        if nodo_actual is None:
            break

        for vecino, peso in grafo[nodo_actual].items():
            if peso > 0 and vecino not in conjunto_visitado:
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    rutas[vecino] = nodo_actual

        conjunto_visitado.add(nodo_actual)

    return distancias, rutas

def reconstruir_camino(rutas, origen, destino):
    camino = []
    nodo = destino

    while nodo != origen:
        if rutas[nodo] is None:
            return None
        camino.append(nodo)
        nodo = rutas[nodo]

    camino.append(origen)
    camino.reverse()

    return camino

# Definir origen y destino
origen = 'ColoniaA'
destino = 'Destino'

distancias_finales, rutas_finales = encontrar_camino_mas_corto(matriz_adyacente, origen)
resultado_camino = reconstruir_camino(rutas_finales, origen, destino)

if resultado_camino:
    print(f"El camino más corto desde '{origen}' hasta '{destino}' es: {' -> '.join(resultado_camino)}")
    print(f"Distancia total: {distancias_finales[destino]} km")
else:
    print(f"No existe un camino desde '{origen}' hasta '{destino}'.")
