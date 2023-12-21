"""

Proyecto final - Introducción a la IA

John Jader Marulanda Valero - 2060034
Joann Esteban Bedoya Lopez - 2059906
Carlos Eduardo Guerrero Jaramillo - 2060216

Universidad del Valle Sede Tuluá
Ingeniería de Sistemas - 3743

"""

import numpy as np
import minmax
import copy

# ----------------- Movements ------------------------


# evalua si la posicion no se sale de la matriz
def overflowCheck(matrix, array):
    maxX = len(matrix[0])
    minX = 0
    maxY = len(matrix)
    minY = 0
    if array[1] >= minX and array[1] < maxX and array[0] >= minY and array[0] < maxY:
        return True
    else:
        return False


# evalua si la posicion de destino esta libre
def positionCheck(matrix, coordTo):
    if matrix[coordTo[0]][coordTo[1]] == 0:
        return True
    elif coordTo[1] in [0, 7]:
        # Permitir que la posición esté ocupada en las columnas extremas
        return True
    else:
        print("Regla: La posicion final debe estar vacia")
        return False


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


# calcula el numero de movimientos segunda jugada, se pasa la matriz una vez hecha el moviento
def getSecondMovement(matrix, position):
    contador = 0
    for fila in matrix:
        if fila[position] != 0:
            contador += 1
    return contador


def checkSecondTurn(subTurn, movement):
    if subTurn == 2 and movement == 0:
        return True
    else:
        return False


# ----------------- GameRules ------------------------


# evalua si la jugada esta dentro de los movimientos posibles en este turno
def ruleMaxMovements(coordFrom, coordTo, maxMovements):
    if (abs(coordFrom[1] - coordTo[1])) == maxMovements:
        return True
    else:
        print("La pieza debe moverse exactamente: " + str(maxMovements) + " casillas")
        return False


# evalua si el jugador se mueve a otra columna y no se devuelva
def ruleNoComeBack(coordFrom, coordTo, turn):
    if turn == 1 and coordFrom[1] < coordTo[1]:
        return True
    if turn == 2 and coordFrom[1] > coordTo[1]:
        return True
    else:
        print("Regla: Se tiene que mover a otra columna y no se puede devolver.")
        return False


# evalua si el jugador del turno actual mueve su pieza y no la del contrincante
# def ruleOnlyMoveYourPeace(piece, turn):
#     if piece == turn:
#         return True
#     else:
#         print("Regla: No puedes mover la pieza de tu contrincante")
#         return False


def ruleOnlyMoveYourPeace(piece, turn):
    if piece == turn:
        return True
    elif piece == 0:  # Agrega esta condición para celdas vacías
        print("Movimiento no válido: No estas seleccionando niguna ficha.")
        return False
    else:
        print("Regla: no puedes mover la pieza de tu contrincante.")
        return False


def inputPlayer(coordFrom, coordTo):
    return 0


def inputOpponent():
    return 0


def ruleNoSecondMovementLast(coordTo, turn):
    if turn == 1 and coordTo[1] == 7:
        return True
    elif turn == 2 and coordTo[1] == 0:
        return True
    else:
        return False


def ruleLastColumnSecondMove(coordFrom, coordTo, movements):
    if coordTo[1] == 7 and movements > (coordTo[1] - coordFrom[1]):
        return True
    else:
        return False


# ----------------- Gameplay ------------------------


# funcion para mover una pieza
def move(matrix, coordFrom, coordTo):
    matrix = movePiece(matrix, coordFrom, coordTo)
    return matrix


def turns(matrix, coordFrom, coordTo, turn, subTurn, movements, depth=3):
    # Turno del jugador 1
    if (
        turn == 1
        and overflowCheck(matrix, coordFrom)
        and overflowCheck(matrix, coordTo)
        and (positionCheck(matrix, coordTo) or ruleNoSecondMovementLast(coordTo, turn))
        and ruleNoComeBack(coordFrom, coordTo, turn)
        and (
            ruleLastColumnSecondMove(coordFrom, coordTo, movements)
            or ruleMaxMovements(coordFrom, coordTo, movements)
        )
    ):
        # Se ve en que jugada esta
        if (
            subTurn == 1
        ):  # Primera jugada. la tercera jugada es si cae en el movimiento especial
            movements = getSecondMovement(matrix, coordTo[1])
            subTurn = 2
        else:
            subTurn = 1  # Resetea subturn
            movements = 1  # movimientos a 1 para el proximo jugador
            turn = 2  # Sigueitne jugador
            print("turno jugador " + str(turn))

        # NO hay segundo movimiento
        print(coordTo)
        if movements == 0 or ruleNoSecondMovementLast(coordTo, turn):
            turn = 2  # Sigueitne jugador
            subTurn = 1
            movements = 1
            print("turno jugador " + str(turn))

        return (move(matrix, coordFrom, coordTo)), movements, subTurn, turn

    elif turn == 2:  # Turno de la IA
        print("IA jugando")
        result, coords = minmax.minimax(
            matrix, True, depth, float("-inf"), float("inf"), 2, -movements
        )

        if result:  # Verifica si se devolvió un resultado válido
            if subTurn == 1:
                # Asegúrate de que haya coordenadas disponibles
                if coords:
                    movements = getSecondMovement(matrix, coords[1][1])
                    subTurn = 2
                else:
                    print("El juego ha terminado.")
                    return matrix, movements, subTurn, turn
            else:
                subTurn = 1
                movements = 1
                turn = 1
                print("turno jugador " + str(turn))

            if movements == 0:
                turn = 1
                print("turno jugador " + str(turn))

            return move(matrix, coords[0], coords[1]), movements, subTurn, turn
        else:
            # Si la IA no puede hacer un movimiento, termina el juego
            print("El juego ha terminado.")
            return matrix, movements, subTurn, turn
    return matrix, movements, subTurn, turn


# ----------------- Puntajes ------------------------


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
