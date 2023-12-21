import numpy as np
import copy


left_column_accumulated = []  # Lista para la columna izquierda (columna 0)
right_column_accumulated = []  # Lista para la columna derecha (columna 7)


# mueve la pieza de la posición de coordFrom a la posición de coordTo en la matriz del tablero
def movePiece(matrix, coordFrom, coordTo):
    # Verificar si la columna de destino está llena
    if matrix[coordTo[0]][coordTo[1]] != 0:
        # La columna de destino está llena

        # Si la columna de destino es la columna izquierda (0), agregar la ficha eliminada a la acumulación izquierda
        if coordTo[1] == 0:
            left_column_accumulated.append(matrix[coordFrom[0]][coordFrom[1]])
        # Si la columna de destino es la columna derecha (7), agregar la ficha eliminada a la acumulación derecha
        elif coordTo[1] == 7:
            right_column_accumulated.append(matrix[coordFrom[0]][coordFrom[1]])

        # Eliminar la ficha del tablero (colocar un 0 en la posición de coordFrom)
        matrix[coordFrom[0]][coordFrom[1]] = 0
    else:
        # La columna de destino no está llena, realizar el movimiento normal

        # Mover la ficha de coordFrom a coordTo
        matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
        # Dejar la posición de coordFrom vacía (colocar un 0)
        matrix[coordFrom[0]][coordFrom[1]] = 0

    # Devolver la matriz actualizada después de realizar el movimiento
    return matrix


# verifica si la columna tiene al menos una posición con valor 0 y devuelve la celda vacía más arriba
def findZeroColumn(matrix, column, movements):
    # Determinar la columna objetivo, limitándola a los índices válidos
    target_column = min(len(matrix[0]) - 1, max(0, column + movements))

    # Iterar a través de las filas de la matriz
    for fila, valor in enumerate(matrix):
        # Verificar si la celda en la columna objetivo tiene valor 0
        if valor[target_column] == 0:
            # Devolver las coordenadas de la celda vacía más arriba
            return [fila, target_column]

    # Si no se encuentra ninguna celda vacía, devolver False
    return False


# recorre toda la matriz y verifica que las fichas tengan el mismo turno, calcula todos los posibles movimientos
# retorna una lista de matrices y coordenadas
def getPosibleMatrices(matrix, movements, turn):
    matrices = (
        []
    )  # Lista para almacenar las matrices resultantes de los posibles movimientos
    coords = []  # Lista para almacenar las coordenadas de los movimientos

    aux = None  # Variable auxiliar para almacenar temporalmente una matriz

    # Iterar a través de las filas y columnas de la matriz
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # Verificar si la ficha en la posición actual tiene el mismo turno y no está en la columna 0
            if matrix[i][j] == turn and j != 0:
                # Encontrar la primera columna vacía a la izquierda de la ficha actual
                aux = findZeroColumn(copy.deepcopy(matrix), j, movements)
                # Si se encuentra una columna vacía, agregar la matriz resultante y las coordenadas a las listas
                if aux:
                    matrices.append(movePiece(copy.deepcopy(matrix), [i, j], aux))
                    coords.append([[i, j], aux])  # coordFrom, coordTo

    # Devolver las listas de matrices y coordenadas
    return matrices, coords


def calculate_scores(matriz):
    # Puntajes por columna para fichas rojas y negras
    red_scores_per_column = [0, 0, 0, 1, 2, 3, 5, 5]
    black_scores_per_column = [5, 3, 2, 1, 0, 0, 0, 0]

    # Inicializar los puntajes
    red_score = 0
    black_score = 0
    winner = None

    # Recorrer cada columna
    for col_idx in range(len(matriz[0])):
        # Contar la cantidad de fichas rojas y negras en la columna
        count_red = sum(1 for fila in matriz if fila[col_idx] == 1)
        count_black = sum(1 for fila in matriz if fila[col_idx] == 2)

        # Sumar las fichas acumuladas en las columnas izquierda y derecha
        count_red += left_column_accumulated[: col_idx + 1].count(1)
        count_black += left_column_accumulated[: col_idx + 1].count(2)

        count_red += right_column_accumulated[col_idx:].count(1)
        count_black += right_column_accumulated[col_idx:].count(2)

        # Actualizar los puntajes según las reglas por columna para fichas rojas y negras
        red_score += count_red * red_scores_per_column[col_idx]
        black_score += count_black * black_scores_per_column[col_idx]

    # Determinar al ganador
    if red_score > black_score:
        winner = 1
    elif black_score > red_score:
        winner = 2
    else:
        winner = 0

    # Devolver los puntajes y al ganador
    return red_score, black_score, winner



def game_over(matrix):
    # Conjuntos para almacenar las columnas ocupadas por fichas rojas y negras
    red_columns = set()
    black_columns = set()

    # Iterar a través de la matriz del tablero
    for fila in matrix:
        for col, valor in enumerate(fila):
            # Si la celda contiene una ficha roja, agregar la columna a red_columns
            if valor == 1:
                red_columns.add(col)
            # Si la celda contiene una ficha negra, agregar la columna a black_columns
            elif valor == 2:
                black_columns.add(col)

    # Verificar si no hay columnas compartidas entre fichas rojas y negras
    # Si no hay intersección, significa que cada jugador tiene sus propias columnas y el juego ha terminado
    return not bool(red_columns.intersection(black_columns))


# Obtiene los scores de una matriz puntual
def getListOfScores(matrices):
    scores = []
    for i in range(len(matrices)):
        scores.append(calculate_scores(matrices[i]))
    return scores


# de la tupla de los scores se optine la que tenga puntaje maximo
# la heuristica es (puntajeRoja < puntajeNegra)
# TODO: esto hace lo mismo que la heuristica (puntajeNegra - puntajeRoja), se puede cambiar si es necesario
def find_max_position(tuple_list, turn):
    if not tuple_list:
        return None  # Return None if the list is empty

    max_value = tuple_list[0][0]
    max_position = 0

    for i, tpl in enumerate(tuple_list):
        if tpl[turn - 1] > max_value and (tpl[2] == turn or tpl[2] == 0):
            max_value = tpl[0]
            max_position = i

    return max_position


# Función de evaluación para la posición actual
def evaluate_position(matrix, turn):
    # Calcular los puntajes de los jugadores a partir de la matriz del tablero
    red_score, black_score, _ = calculate_scores(matrix)

    # Devolver la diferencia de puntajes, dependiendo del turno del jugador actual
    # Si es el turno del jugador negro (turn == 2), se resta el puntaje de las fichas rojas
    # Si es el turno del jugador rojo (cualquier otro valor de turn), se resta el puntaje de las fichas negras
    return black_score - red_score if turn == 2 else red_score - black_score


# Definición de la función Minimax
def minimax(matrix, maximizing, depth, turn, movements):
    # Verificar si se alcanzó la profundidad máxima o si el juego ha terminado
    if depth == 0 or game_over(matrix):
        # Calcular la evaluación de la posición actual y devolverla junto con None (sin movimiento)
        return evaluate_position(matrix, turn), None

    # Obtener las posibles matrices y las coordenadas correspondientes a los movimientos válidos
    posibles, coords = getPosibleMatrices(matrix, movements, turn)

    # Si es el turno de maximizar
    if maximizing:
        maxEval = float("-inf")  # Inicializar la mejor evaluación como menos infinito
        # Esto se hace para asegurar que cualquier evaluación encontrada durante la búsqueda
        # sea considerada inicialmente como mejor que la evaluación actual.
        best_move = None  # Inicializar la mejor jugada como None
        # Iterar sobre las posibles matrices y sus coordenadas
        for i, move in enumerate(posibles):
            # Llamar recursivamente a minimax con el nuevo movimiento y cambiar el turno
            evaluation, _ = minimax(move, False, depth - 1, turn, movements)
            # Actualizar la mejor evaluación y la mejor jugada si se encuentra una evaluación mejor
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = coords[i]
        # Devolver la mejor evaluación y la mejor jugada
        return maxEval, best_move
    else:  # Si es el turno de minimizar
        minEval = float("inf")  # Inicializar la mejor evaluación como infinito
        # Esto se hace para asegurar que cualquier evaluación encontrada durante la búsqueda
        # sea considerada inicialmente como la peor evaluación posible.
        best_move = None  # Inicializar la mejor jugada como None
        # Iterar sobre las posibles matrices y sus coordenadas
        for i, move in enumerate(posibles):
            # Llamar recursivamente a minimax con el nuevo movimiento y cambiar el turno
            evaluation, _ = minimax(move, True, depth - 1, turn, movements)
            # Actualizar la mejor evaluación y la mejor jugada si se encuentra una evaluación mejor
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = coords[i]
        # Devolver la mejor evaluación y la mejor jugada
        return minEval, best_move


# matrix = [
#     [1, 1, 1, 1, 1, 1, 1, 2],
#     [1, 0, 0, 0, 0, 0, 0, 2],
#     [1, 0, 0, 0, 0, 0, 0, 2],
#     [1, 0, 0, 0, 0, 0, 0, 2],
#     [1, 0, 0, 0, 0, 0, 0, 2],
#     [1, 2, 2, 2, 2, 2, 2, 2],
# ]

# posibles = getPosibleMatrices(matrix, 1, 1)
# print(getListOfScores(posibles))

# print(np.array(minimax(matrix, True, 2, -1)))
