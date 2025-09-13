#Actividad_2_Árbol_de_expansión_a_lo_ancho_Actividad_modificada
import csv

# Leer el archivo CSV
def leer_grafo_csv(archivo_csv):
    grafos = {}
    with open(archivo_csv, 'r') as archivo:
        lector = csv.reader(archivo)
        encabezados = next(lector)  # Nombres de los vértices
        for fila in lector:
            vertice = fila[0]
            grafos[vertice] = {encabezados[i]: float(fila[i]) if fila[i] else 0 for i in range(1, len(fila))}
    return grafos

# Ruta al archivo CSV
ruta_csv = "colonias.csv"
grafos = leer_grafo_csv(ruta_csv)

# Algoritmo para árbol de expansión
def be(V, E):
    Vp = {V[0]}  # Conjunto de vértices conectados
    Ep = []      # Lista de aristas del árbol
    w = V[0]     # Nodo inicial

    while True:
        while True:
            arista_minima = None
            for vK in V:
                if vK in Vp:
                    continue
                if grafos[w][vK] > 0:
                    if not arista_minima or grafos[w][vK] < grafos[arista_minima[0]][arista_minima[1]]:
                        arista_minima = (w, vK)

            if arista_minima: 
                w, vK = arista_minima
                Ep.append((w, vK, grafos[w][vK]))  # Guardamos también la distancia
                Vp.add(vK)
                w = vK
            else:
                break
        if w == V[0]:
            return Ep, Vp
        for u, v, _ in Ep[::-1]:
            if v == w:
                w = u
                break

# Extraer los vértices
V = list(grafos.keys())
E = []

# Ejecutar el algoritmo
arbol_expansion = be(V, E)

# Imprimir los resultados
print("\nÁrbol de expansión mínimo para conectar colonias:")
for arista in arbol_expansion[0]:
    print(f"{arista[0]} ↔ {arista[1]}  ({arista[2]} km)")

print("\nColonias conectadas:", arbol_expansion[1])
