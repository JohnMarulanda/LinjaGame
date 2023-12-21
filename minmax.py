
import numpy as np
import copy


left_column_accumulated = []  # Lista para la columna izquierda (columna 0)
right_column_accumulated = []  # Lista para la columna derecha (columna 7)


# mueve la pieza de posicion
def movePiece(matrix, coordFrom, coordTo):
    if matrix[coordTo[0]][coordTo[1]] != 0:
        # La columna de destino está llena
        if coordTo[1] == 0:
            left_column_accumulated.append(matrix[coordFrom[0]][coordFrom[1]])
        elif coordTo[1] == 7:
            right_column_accumulated.append(matrix[coordFrom[0]][coordFrom[1]])

        # Eliminar la ficha del tablero
        matrix[coordFrom[0]][coordFrom[1]] = 0
    else:
        # La columna de destino no está llena, realizar el movimiento normal
        matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
        matrix[coordFrom[0]][coordFrom[1]] = 0

    return matrix

# ve si la columna tiene almenos una posicion en 0 y la retorna la cacilla vacia mas arriba
def findZeroColumn(matrix, column, movements):
    target_column = min(len(matrix[0]) - 1, max(0, column + movements))

    for fila, valor in enumerate(matrix):
        if valor[target_column] == 0:
            return [fila, target_column]
    return False

# recorre toda la matriz y ve que turn son iguales, calcula todos los posibles movimientos
# retorna list matrices y coords
def getPosibleMatrices(matrix, movements, turn):
    matrices = []
    coords = []
    aux = None
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == turn and j != 0:
                aux = findZeroColumn(copy.deepcopy(matrix), j, movements)
                if aux:
                    matrices.append(movePiece(copy.deepcopy(matrix), [i, j], aux))
                    coords.append([[i, j], aux])  # coordFrom, coordTo

    return matrices, coords


def calculate_scores(matriz):
    # Inicializar los puntajes
    red_score = 0
    black_score = 0
    winner = None

    # Definir los puntajes por columna
    scores_per_column = [5, 3, 2, 1, 1, 2, 3, 5]

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

        # Actualizar los puntajes según las reglas
        red_score += count_red * scores_per_column[col_idx]
        black_score += count_black * scores_per_column[col_idx]

    # Determinar al ganador
    if red_score > black_score:
        winner = 1
    elif black_score > red_score:
        winner = 2
    else:
        winner = 0

    return red_score, black_score, winner


def game_over(matriz):
    # Verifica si las fichas rojas y negras no comparten ninguna columna
    red_columns = set()
    black_columns = set()

    for fila in matriz:
        for col, valor in enumerate(fila):
            if valor == 1:
                red_columns.add(col)
            elif valor == 2:
                black_columns.add(col)

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


# La ia siempre tratara de maximizar
def minimax(matrix, maximizing, turn, movements):
    posibles, coords = getPosibleMatrices(
        matrix, movements, turn
    )  # retorna una lista de matrices

    # llamamos a game_over para evaluar si el juego ha finalizado
    if game_over(matrix):
        return None

    socresList = getListOfScores(posibles)
    if maximizing:
        position = find_max_position(socresList, turn)
        return posibles[position], coords[position]
    else:
        return False


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
