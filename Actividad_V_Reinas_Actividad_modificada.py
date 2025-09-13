#Actividad_V_Reinas_Actividad_modificada 
def existe_conflicto(posiciones, hora):
    for h in range(1, hora):  
        # Misma sala o conflicto de horario consecutivo (simula diagonal)
        if posiciones[h] == posiciones[hora] or abs(posiciones[h] - posiciones[hora]) == abs(h - hora):
            return True
    return False

def asignar_reuniones():
    posiciones = [0] * 6  # columnas: horas 1 a 5 (usamos índice 1-5)
    hora_actual = 1
    posiciones[hora_actual] = 0

    while hora_actual > 0:
        if hora_actual >= len(posiciones):
            hora_actual -= 1
            continue
        
        posiciones[hora_actual] += 1  # Intentar siguiente sala en la hora actual
        
        while posiciones[hora_actual] <= 5 and existe_conflicto(posiciones, hora_actual):
            posiciones[hora_actual] += 1  

        if posiciones[hora_actual] <= 5:
            if hora_actual == 5:  # Si se asignaron todas las horas
                return True, posiciones[1:6]  # Devolver solución (horas 1-5)
            else:
                hora_actual += 1
                if hora_actual < len(posiciones):
                    posiciones[hora_actual] = 0
        else:
            hora_actual -= 1  # Retroceder si no hay más salas válidas

    return False, []

# Ejecutar la asignación
exito, asignacion = asignar_reuniones()

# Mostrar resultados
if exito:
    print("Asignación de reuniones encontrada (sala por hora):", asignacion)
else:
    print("No se pudo encontrar una asignación válida.")
