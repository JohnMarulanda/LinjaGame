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


# evalúa si la posición representada por el array no se sale de los límites de la matriz
def overflowCheck(matrix, array):
    maxX = len(matrix[0])  # Obtener el número máximo de columnas
    minX = 0  # El número mínimo de columnas generalmente es 0
    maxY = len(matrix)  # Obtener el número máximo de filas
    minY = 0  # El número mínimo de filas generalmente es 0

    # Verificar si la posición representada por el array está dentro de los límites de la matriz
    if array[1] >= minX and array[1] < maxX and array[0] >= minY and array[0] < maxY:
        return True  # La posición está dentro de los límites
    else:
        return False  # La posición está fuera de los límites


# evalúa si la posición de destino representada por coordTo está libre en la matriz
def positionCheck(matrix, coordTo):
    # Verificar si la posición de destino está vacía
    if matrix[coordTo[0]][coordTo[1]] == 0:
        return True  # La posición de destino está libre
    elif coordTo[1] in [0, 7]:
        # Permitir que la posición esté ocupada en las columnas extremas
        return True
    else:
        print("Regla: La posición final debe estar vacía")
        return False  # La posición de destino no está libre


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

    return matrix


# calcula el número de movimientos después de la segunda jugada, se pasa la matriz después de realizar el movimiento
def getSecondMovement(matrix, position):
    contador = 0  # Inicializar el contador de fichas en la columna especificada

    # Iterar a través de las filas de la matriz
    for fila in matrix:
        # Incrementar el contador si la celda en la columna especificada no es 0 (contiene una ficha)
        if fila[position] != 0:
            contador += 1

    # Devolver el número de fichas en la columna después del movimiento
    return contador


# verifica si es el segundo turno del juego y el número de movimientos es igual a 0
def checkSecondTurn(subTurn, movement):
    if subTurn == 2 and movement == 0:
        return True  # Es el segundo turno y el número de movimientos es 0
    else:
        return False  # No es el segundo turno o el número de movimientos no es 0


# ----------------- GameRules ------------------------


# evalúa si la jugada está dentro de los movimientos posibles en este turno
def ruleMaxMovements(coordFrom, coordTo, maxMovements):
    # Verificar si la distancia horizontal entre coordFrom y coordTo es igual a maxMovements
    if (abs(coordFrom[1] - coordTo[1])) == maxMovements:
        return True  # La jugada está dentro de los movimientos posibles
    else:
        print("La pieza debe moverse exactamente: " + str(maxMovements) + " casillas")
        return False  # La jugada no cumple con la restricción de movimientos


# evalúa si el jugador se mueve a otra columna y no se devuelve en el mismo turno
def ruleNoComeBack(coordFrom, coordTo, turn):
    # Verificar si el jugador 1 se mueve hacia la derecha y el jugador 2 se mueve hacia la izquierda
    if turn == 1 and coordFrom[1] < coordTo[1]:
        return True  # Jugador 1 se mueve hacia la derecha
    # Verificar si el jugador 2 se mueve hacia la izquierda y el jugador 1 se mueve hacia la derecha
    elif turn == 2 and coordFrom[1] > coordTo[1]:
        return True  # Jugador 2 se mueve hacia la izquierda
    else:
        print("Regla: Se tiene que mover a otra columna y no se puede devolver.")
        return False  # La jugada no cumple con la restricción de no devolverse en el mismo turno


# evalúa si el jugador puede mover la pieza específica en función de su turno
def ruleOnlyMoveYourPeace(piece, turn):
    # Verificar si la pieza seleccionada pertenece al jugador actual (turn)
    if piece == turn:
        return True  # El jugador puede mover su propia pieza
    elif piece == 0:  # Agrega esta condición para celdas vacías
        print("Movimiento no válido: No estás seleccionando ninguna ficha.")
        return False  # La celda seleccionada está vacía, no se puede mover
    else:
        print("Regla: No puedes mover la pieza de tu contrincante.")
        return False  # El jugador no puede mover la pieza del contrincante


def inputPlayer(coordFrom, coordTo):
    return 0


def inputOpponent():
    return 0


# evalúa si el jugador no puede realizar un segundo movimiento en la última columna del tablero
def ruleNoSecondMovementLast(coordTo, turn):
    # Verificar si el jugador 1 no puede realizar un segundo movimiento en la última columna
    if turn == 1 and coordTo[1] == 7:
        return True  # Jugador 1 no puede realizar un segundo movimiento en la última columna
    # Verificar si el jugador 2 no puede realizar un segundo movimiento en la primera columna
    elif turn == 2 and coordTo[1] == 0:
        return True  # Jugador 2 no puede realizar un segundo movimiento en la primera columna
    else:
        return False  # El jugador puede realizar un segundo movimiento en la última columna


# evalúa si el jugador puede realizar un segundo movimiento en la última columna del tablero
def ruleLastColumnSecondMove(coordFrom, coordTo, movements):
    # Verificar si el jugador se mueve a la última columna y el número de movimientos es suficiente
    if coordTo[1] == 7 and movements > (coordTo[1] - coordFrom[1]):
        return (
            True  # El jugador puede realizar un segundo movimiento en la última columna
        )
    else:
        return False  # El jugador no cumple con la regla para realizar un segundo movimiento en la última columna


# ----------------- Gameplay ------------------------


# función para mover una pieza en la matriz
def move(matrix, coordFrom, coordTo):
    # Utilizar la función movePiece para realizar el movimiento de la pieza en la matriz
    matrix = movePiece(matrix, coordFrom, coordTo)
    # Devolver la matriz actualizada después de realizar el movimiento
    return matrix


def turns(matrix, coordFrom, coordTo, turn, subTurn, movements, depth=3):
    # Turno del jugador 1
    if (
        turn == 1
        and overflowCheck(
            matrix, coordFrom
        )  # Verificar desbordamiento en las coordenadas de origen
        and overflowCheck(
            matrix, coordTo
        )  # Verificar desbordamiento en las coordenadas de destino
        and (
            positionCheck(matrix, coordTo) or ruleNoSecondMovementLast(coordTo, turn)
        )  # Verificar posición válida o movimiento especial
        and ruleNoComeBack(
            coordFrom, coordTo, turn
        )  # Verificar regla de no devolverse en el mismo turno
        and (
            ruleLastColumnSecondMove(
                coordFrom, coordTo, movements
            )  # Verificar regla de segundo movimiento en la última columna
            or ruleMaxMovements(
                coordFrom, coordTo, movements
            )  # Verificar regla de máximo de movimientos permitidos
        )
    ):
        # Se verifica en qué jugada está
        if subTurn == 1:
            # Primera jugada. La tercera jugada es si cae en el movimiento especial
            movements = getSecondMovement(matrix, coordTo[1])
            subTurn = 2
        else:
            subTurn = 1  # Resetea subturn
            movements = 1  # Movimientos a 1 para el próximo jugador
            turn = 2  # Siguiente jugador
            print("turno jugador " + str(turn))

        # No hay segundo movimiento
        print(coordTo)
        if movements == 0 or ruleNoSecondMovementLast(coordTo, turn):
            turn = 2  # Siguiente jugador
            subTurn = 1
            movements = 1
            print("turno jugador " + str(turn))

        return move(matrix, coordFrom, coordTo), movements, subTurn, turn

    # Turno de la IA
    elif turn == 2:
        print("IA jugando")
        result, coords = minmax.minimax(matrix, True, depth, 2, -movements)

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
                movements = 1
                subTurn = 1
                turn = 1
                print("turno jugador " + str(turn))

            return move(matrix, coords[0], coords[1]), movements, subTurn, turn
        else:
            # Si la IA no puede hacer un movimiento, termina el juego
            print("El juego ha terminado.")
            return matrix, movements, subTurn, turn

    # Si no se cumplen las condiciones anteriores, devolver el estado actual del juego
    return matrix, movements, subTurn, turn


# ----------------- Puntajes ------------------------


def calculate_scores(matriz):
    # Puntajes por columna para fichas rojas y negras
    red_scores_per_column = [0, 0, 0, 0, 1, 2, 3, 5]
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

