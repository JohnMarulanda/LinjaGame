'''

Proyecto final - Introducción a la IA

John Jader Marulanda Valero - 2060034
Joann Esteban Bedoya Lopez - 2059906
Carlos Eduardo Guerrero Jaramillo - 2060216

Universidad del Valle Sede Tuluá
Ingeniería de Sistemas - 3743

'''

def calcular_movimientos_posibles(matriz):
    movimientos = []

    for fila_idx, fila in enumerate(matriz):
        for col_idx, casilla in enumerate(fila):
            if casilla == 1 or casilla == 2:
                # Si la casilla contiene una ficha roja o negra
                # Revisar movimientos posibles hacia la derecha o izquierda
                if col_idx > 0 and fila[col_idx - 1] == 0:
                    movimientos.append(((fila_idx, col_idx), (fila_idx, col_idx - 1)))
                if col_idx < len(fila) - 1 and fila[col_idx + 1] == 0:
                    movimientos.append(((fila_idx, col_idx), (fila_idx, col_idx + 1)))

    return movimientos

def minimax(matriz, profundidad, es_maximizando):
    puntuacion = evaluar_estado(matriz)

    # Condiciones de parada (estado terminal o profundidad máxima)
    if puntuacion != 0 or profundidad == 0:
        return puntuacion

    if es_maximizando:
        mejor_valor = float('-inf')
        movimientos = calcular_movimientos_posibles(matriz)
        for movimiento in movimientos:
            # Realizar el movimiento
            nuevo_estado = realizar_movimiento(matriz, movimiento)
            valor = minimax(nuevo_estado, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        movimientos = calcular_movimientos_posibles(matriz)
        for movimiento in movimientos:
            # Realizar el movimiento
            nuevo_estado = realizar_movimiento(matriz, movimiento)
            valor = minimax(nuevo_estado, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def mejor_movimiento(matriz, profundidad):
    mejor_valor = float('-inf')
    mejor_movimiento = None
    movimientos = calcular_movimientos_posibles(matriz)
    for movimiento in movimientos:
        nuevo_estado = realizar_movimiento(matriz, movimiento)
        valor = minimax(nuevo_estado, profundidad - 1, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento

def evaluar_estado(matriz):
    # Verificar que cada fila contenga al menos una pieza
    for fila in matriz:
        if not any(c != 0 for c in fila):
            return False

    # Verificar que no se puedan mover más de 6 piezas en un solo movimiento
    for fila in matriz:
        if sum(c != 0 for c in fila) > 6:
            return False

    # Verificar que no se pueda mover una pieza a una fila vacía
    if not all(matriz[-1]):
        return False

    return True

def realizar_movimiento(matriz, movimiento):
    origen, destino = movimiento

    fila_origen, col_origen = origen
    fila_destino, col_destino = destino

    if matriz[fila_origen][col_origen] == 0 or matriz[fila_destino][col_destino] != 0:
        return matriz  # Devolver el mismo estado si el movimiento no es válido

    # Realizar el movimiento actualizando la matriz
    matriz[fila_destino][col_destino] = matriz[fila_origen][col_origen]
    matriz[fila_origen][col_origen] = 0

    return matriz


def main():
    # Estado inicial del juego
    matriz_inicial = [
        [1, 1, 1, 1, 1, 1, 1, 2],
        [1, 0, 0, 0, 0, 0, 0, 2],
        [1, 0, 0, 0, 0, 0, 0, 2],
        [1, 0, 0, 0, 0, 0, 0, 2],
        [1, 0, 0, 0, 0, 0, 0, 2],
        [1, 2, 2, 2, 2, 2, 2, 2]
        ]

    # Profundidad de búsqueda
    profundidad = 3

    # Obtener el mejor movimiento
    movimiento = mejor_movimiento(matriz_inicial, profundidad)

    # Imprimir el movimiento
    print(movimiento)


if __name__ == "__main__":
    main()
