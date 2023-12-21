
import numpy as np
import copy


# funcion game_over cuando ninguna ficha comparte columna
def game_over(matrix):
    # Recorrer cada columna del tablero
    for col_idx in range(len(matrix[0])):
        column_values = [matrix[row_idx][col_idx] for row_idx in range(len(matrix))]
        # Si todas las celdas de la columna no son iguales (no hay fichas compartidas)
        if len(set(column_values)) == len(column_values):
            return True
    return False



# mueve la pieza de posicion
def movePiece(matrix, coordFrom, coordTo):
    matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
    matrix[coordFrom[0]][coordFrom[1]] = 0
    return matrix

# ve si la columna tiene almenos una posicion en 0 y la retorna la cacilla vacia mas arriba
def findZeroColumn(matrix, column):
    for fila, valor in enumerate(matrix):
        if valor[column] == 0:
            return [fila, column]
    return False

# recorre toda la matriz y ve que turn son iguales, calcula todos los posibles movimientos
# retorna list matrices y coords
def getPosibleMatrices(matrix, movements, turn):# movement es un numero
    matrices = []
    coords = []
    aux = None
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == turn:
                aux = findZeroColumn(copy.deepcopy(matrix), j+movements)
                if aux:
                    matrices.append(movePiece(copy.deepcopy(matrix), [i, j], aux))
                    coords.append([[i, j], aux]) #coordFrom, coordTo

    return matrices, coords

# calcula los puntajes de cada color
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
        if tpl[turn-1] > max_value and (tpl[2] == turn or tpl[2] == 0):
            max_value = tpl[0]
            max_position = i

    return max_position

#La ia siempre tratara de maximizar
def minimax(matrix, maximizing, turn, movements):
    posibles, coords = getPosibleMatrices(matrix, movements, turn) # retorna una lista de matrices

    # llamamos a game_over para evaluar si el juego ha finalizado
    if game_over(matrix):
        return None

    socresList = getListOfScores(posibles)
    if maximizing:
        position = find_max_position(socresList, turn)
        return posibles[position], coords[position]
    else:
        return False


matrix = [
    [1, 1, 1, 1, 1, 1, 1, 2], 
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 2, 2, 2, 2, 2, 2, 2]
]

#posibles = getPosibleMatrices(matrix, 1, 1)
#print(getListOfScores(posibles))

#print(np.array(minimax(matrix, True, 2, -1)))