
import numpy as np
import copy

# mueve la pieza de posicion
def movePiece(matrix, coordFrom, coordTo):
    matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
    matrix[coordFrom[0]][coordFrom[1]] = 0
    return matrix

def findZeroColumn(matrix, column):
    for fila, valor in enumerate(matrix):
        if valor[column] == 0:
            return [fila, column]
    return False

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


def getListOfScores(matrices):
    scores = []
    for i in range(len(matrices)):
        scores.append(calculate_scores(matrices[i]))
    return scores

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