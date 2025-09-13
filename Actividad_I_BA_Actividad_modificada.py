#Actividad_I_BA_Actividad_modificada
# Búsqueda en Amplitud (BA) aplicada a estaciones de metro
from collections import deque

def bfs_tree(B, E, r):
    tB = {r}  # Estaciones alcanzadas
    tE = set()   # Conexiones recorridas
    S = deque([r])  # Orden de exploración

    while True:
        added_edge = False

        for x in list(S):  # Recorremos las estaciones en la cola
            for y in B:
                if y not in tB and (x, y) in E:
                    tE.add((x, y))
                    tB.add(y)
                    S.append(y)
                    added_edge = True
        
        if not added_edge:
            return tB, tE
        # Ordenar la cola para seguir el orden de las estaciones
        S = deque(sorted(S, key=lambda v: B.index(v)))


# Lista de estaciones de metro
B = ['Insurgentes', 'Revolución', 'Hidalgo', 'Zócalo', 'Balderas', 'Tacuba', 'Chapultepec', 'Centro Médico']

# Conexiones entre estaciones (aristas)
E = {
    ('Insurgentes', 'Revolución'),
    ('Revolución', 'Hidalgo'),
    ('Hidalgo', 'Zócalo'),
    ('Insurgentes', 'Balderas'),
    ('Balderas', 'Centro Médico'),
    ('Chapultepec', 'Insurgentes'),
    ('Tacuba', 'Chapultepec'),
    ('Hidalgo', 'Tacuba')
}

# Estación inicial
r = 'Insurgentes'

# Ejecutar BFS
tB, tE = bfs_tree(B, E, r)

# Mostrar resultados
print("Estaciones alcanzadas desde", r, ":", tB)
print("Conexiones recorridas:", tE)
