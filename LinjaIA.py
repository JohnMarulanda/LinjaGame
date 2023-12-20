'''

Proyecto final - Introducción a la IA

John Jader Marulanda Valero - 2060034
Joann Esteban Bedoya Lopez - 2059906
Carlos Eduardo Guerrero Jaramillo - 2060216

Universidad del Valle Sede Tuluá
Ingeniería de Sistemas - 3743

'''

# Encuentra todos los movimientos posibles para un jugador en un estado dado del tablero.
def get_possible_moves(matrix, turn):
    possible_moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Define las direcciones posibles de movimiento

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == turn:  # Encuentra las fichas del jugador actual en el tablero
                for direction in directions:
                    new_y = y + direction[0]
                    new_x = x + direction[1]
                    if 0 <= new_y < len(matrix) and 0 <= new_x < len(matrix[0]):
                        if matrix[new_y][new_x] == 0:  # Verifica si la casilla adyacente está vacía
                            possible_moves.append(((y, x), (new_y, new_x)))  # Agrega el movimiento posible

    return possible_moves

# Evalúa el tablero y asigna un puntaje para cada jugador en función de la posición de sus fichas.
def evaluate_board(matrix):
    red_score = 0
    black_score = 0

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 1:  # Fichas rojas
                red_score += (len(matrix[0]) - 1 - x)  # Aumenta el puntaje si están cerca de la columna opuesta
            elif matrix[y][x] == 2:  # Fichas negras
                black_score += x  # Aumenta el puntaje si están cerca de la columna opuesta

    return black_score - red_score  # Puntuación total para las negras menos la puntuación total para las rojas

# Realiza un movimiento en el tablero si es válido.
def make_move(matrix, coord_from, coord_to, is_black_turn):
    if matrix[coord_to[0]][coord_to[1]] == 0:  # Verifica que el destino esté vacío
        if is_black_turn:
            matrix[coord_to[0]][coord_to[1]] = 2  # Ficha negra
        else:
            matrix[coord_to[0]][coord_to[1]] = 1  # Ficha roja

        matrix[coord_from[0]][coord_from[1]] = 0
        return matrix
    else:
        print("Movimiento inválido: La posición de destino no está vacía.")
        return None  # Devuelve None si el movimiento no es válido

# Cambia el turno del jugador oponente.
# AÚN ESTÁ EN PRUEBA LA FUNCIONALIDAD, PIPOL
def opponent_turn(is_black_turn):
    return not is_black_turn  # Cambia el turno negando el booleano

# Verifica si el juego ha terminado.
# Termina el juego si la fincha de algun jugador llega al extremo
def game_over(matrix):
    black_reached_end = False
    red_reached_end = False

    for x in range(len(matrix[0])):
        if matrix[0][x] == 2:  # Ficha negra llegó a la columna 0
            black_reached_end = True
        if matrix[len(matrix) - 1][x] == 1:  # Ficha roja llegó a la columna opuesta
            red_reached_end = True

    if black_reached_end or red_reached_end:
        return True  # El juego termina si alguna ficha llega al otro extremo del tablero
    else:
        return False


#  Implementa el algoritmo Minimax para encontrar el mejor movimiento en función de un estado dado del tablero.
def minimax(matrix, depth, maximizing_player, turn):
    if depth == 0 or game_over(matrix):
        return evaluate_board(matrix), None  # Devuelve también None para el movimiento

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        possible_moves = get_possible_moves(matrix, turn)
        for move in possible_moves:
            new_board = make_move(matrix, move[0], move[1], turn)
            eval, _ = minimax(new_board, depth - 1, False, opponent_turn(turn))
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move  # Devuelve el mejor movimiento y su evaluación
    else:
        min_eval = float('inf')
        best_move = None
        possible_moves = get_possible_moves(matrix, opponent_turn(turn))
        for move in possible_moves:
            new_board = make_move(matrix, move[0], move[1], opponent_turn(turn))
            eval, _ = minimax(new_board, depth - 1, True, turn)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move  # Devuelve el mejor movimiento y su evaluación
