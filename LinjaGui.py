"""

Proyecto final - Introducción a la IA

John Jader Marulanda Valero - 2060034
Joann Esteban Bedoya Lopez - 2059906
Carlos Eduardo Guerrero Jaramillo - 2060216

Universidad del Valle Sede Tuluá
Ingeniería de Sistemas - 3743

"""

import pygame
import sys
from tkinter import Tk, filedialog
import LinjaController as controller
import time
import copy


# Inicializar Pygame
pygame.init()


"""
Convenciones del tablero:

0 = Espacios de movimiento
1 = Fichas Rojas
2 = Fichas negras
"""

# Variables
m1 = [0, 0]
m2 = [0, 0]
count = 0
turn = 1
subTurn = 1
movements = 1  # Numero de movimientos


def guardar_archivo(matrix):
    root = Tk()
    root.withdraw()

    # Seleccionar la carpeta de destino
    folder_selected = filedialog.askdirectory()

    if folder_selected:
        file_path = (
            folder_selected + "/matrix.txt"
        )  # Ruta para el archivo en la carpeta seleccionada

        # Guardar la matriz en un archivo de texto
        with open(file_path, "w") as file:
            for row in matrix:
                file.write(" ".join(map(str, row)) + "\n")

        print(f"La matriz se ha guardado en {file_path}")


def cargar_archivo():
    root = Tk()
    root.withdraw()  # Evita que se abra una ventana principal de Tkinter
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")],
    )
    root.destroy()

    if not file_path:
        return None

    try:
        with open(file_path, "r") as file:
            # Leer líneas del archivo y contar unos, doses y ceros
            ones_count = 0
            twos_count = 0
            zeros_count = 0
            lines = file.readlines()

            for line in lines:
                row = [int(cell) for cell in line.split()]
                zeros_count += row.count(0)
                ones_count += row.count(1)
                twos_count += row.count(2)

            # Verificar que las dimensiones y la cantidad de unos y doses sean correctas
            if (
                len(lines) == 6
                and len(lines[0].split()) == 8
                and ones_count == 12
                and twos_count == 12
                and zeros_count == (6 * 8 - 24)
            ):
                matrix = [[int(cell) for cell in line.split()] for line in lines]
            else:
                print("Archivo no cumple con las condiciones especificas de LINJA.")
                return None

    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

    return matrix


def obtener_coordenadas(pos):
    x, y = pos
    col = x // cell_width
    row = y // cell_height
    return row, col


# Generación de la matriz
matrix = cargar_archivo()

# Verificar si la carga del archivo fue exitosa
if matrix is None:
    sys.exit()  # Salir del programa si la carga falla

# Tamaño de la ventana
matrix_rows = len(matrix)
matrix_cols = len(matrix[0])

# Ancho de la ventana
window_width = 1000
# Ancho deseado para el juego
desired_game_width = 800

# Calcula el ancho de la celda basado en el ancho deseado del juego
cell_width = desired_game_width // matrix_cols

# Altura de la ventana y altura de la celda
window_height = cell_width * matrix_rows
cell_height = window_height // matrix_rows

# Ancho del área en blanco para botones
blank_width = window_width - desired_game_width

# Crear una superficie aparte
blank_surface = pygame.Surface((blank_width, window_height))
blank_surface.fill((45, 87, 44))  # Rellena el área en blanco con blanco

# Coordenadas y tamaño del nuevo botón (debajo del botón existente)
two_button_rect = pygame.Rect(820, 180, 160, 70)

# Coordenadas y tamaño del nuevo botón (debajo del botón existente)
three_button_rect = pygame.Rect(820, 320, 160, 70)

text_rect = pygame.Rect(
    20, 50, 160, 40
)  # Ajusta las coordenadas y el tamaño según tus necesidades

# Cargar las imágenes del botón
button_unpressed_image = pygame.image.load("Sprites/Play_Unpressed.png")
button_pressed_image = pygame.image.load("Sprites/Play_Pressed.png")


# Cargar las imágenes del botón guardar
button_save_unpressed_image = pygame.image.load("Sprites/Save_Unpressed.png")
button_save_pressed_image = pygame.image.load("Sprites/Save_Pressed.png")

# Escalar las imágenes al tamaño deseado (ancho, alto)
button_unpressed_image = pygame.transform.scale(button_unpressed_image, (160, 70))
button_pressed_image = pygame.transform.scale(button_pressed_image, (160, 70))

# Escalar las imágenes de guardar al tamaño deseado (ancho, alto)
button_save_unpressed_image = pygame.transform.scale(
    button_save_unpressed_image, (160, 70)
)
button_save_pressed_image = pygame.transform.scale(button_save_pressed_image, (160, 70))

# Coordenadas donde dibujar la imagen del botón
button_rect = button_unpressed_image.get_rect()
button_rect.topleft = (20, 180)  # Ajusta las coordenadas según tus necesidades

# Estado actual del botón
button_pressed = False

# Coordenadas donde dibujar la imagen del botón guardar
button_save_rect = button_save_unpressed_image.get_rect()
button_save_rect.topleft = (20, 320)  # Ajusta las coordenadas según tus necesidades

# Estado actual del botón
button_save_pressed = False

# Crear una fuente para el texto
font = pygame.font.Font("Sprites/PokemonGb-RAeo.ttf", 12)  # Tamaño de la fuente
large_font = pygame.font.Font(
    "Sprites/PokemonGb-RAeo.ttf", 24
)  # Tamaño de la fuente grande


# Crear una superficie degradada
gradient_surface = pygame.Surface((blank_width, window_height))
gradient_rect = gradient_surface.get_rect()
color1 = (227, 166, 112)  # Primer color del degradado
color2 = (253, 221, 202)  # Segundo color del degradado

# Llenar la superficie degradada con un degradado
for y in range(gradient_rect.height):
    gradient_ratio = y / gradient_rect.height
    r = int(color1[0] * (1 - gradient_ratio) + color2[0] * gradient_ratio)
    g = int(color1[1] * (1 - gradient_ratio) + color2[1] * gradient_ratio)
    b = int(color1[2] * (1 - gradient_ratio) + color2[2] * gradient_ratio)
    pygame.draw.line(gradient_surface, (r, g, b), (0, y), (gradient_rect.width, y))

# Cargar imágenes
image_dict = {
    0: pygame.image.load("Sprites/Vacio.png"),
    1: pygame.image.load("Sprites/Ficharoja.png"),
    2: pygame.image.load("Sprites/FichaNegra.png"),
}

# Crear la ventana
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Linja - Juego de Estrategia")


# Bucle principal para la interfaz gráfica
running = True
game_over_message_printed = (
    False  # Nuevo flag para evitar imprimir múltiples mensajes de fin de juego
)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and turn == 1:  # turno del jugador
            if two_button_rect.collidepoint(event.pos):
                # Si se presionar cargar archivo dentro del juego
                new_matrix = cargar_archivo()
                if new_matrix:
                    matrix = new_matrix  # Actualizar la matriz del juego con la nuev
                # Cambia el estado del botón
                button_pressed = True
                # Espera un tiempo antes de restaurar el botón a su estado normal
                pygame.time.set_timer(
                    pygame.USEREVENT, 200
                )  # 200 ms (ajusta según tu preferencia)
            elif three_button_rect.collidepoint(event.pos):
                guardar_archivo(matrix)
                # Cambia el estado del botón
                button_save_pressed = True
                # Espera un tiempo antes de restaurar el botón a su estado normal
                pygame.time.set_timer(
                    pygame.USEREVENT, 200
                )  # 200 ms (ajusta según tu preferencia)
            else:
                # Obtener las coordenadas al hacer clic en una celda
                row, col = obtener_coordenadas(event.pos)
                # print(f"Coordenadas: [{row},{col}] = {matrix[row][col]}")

                if count == 0 and controller.ruleOnlyMoveYourPeace(
                    matrix[row][col], turn
                ):
                    # Si count es 0 y la regla permite mover la pieza del jugador actual
                    m1 = [row, col]
                    count = 1
                elif count > 0:
                    # Si count es mayor que 0, se registra la segunda coordenada m2
                    m2 = [row, col]
                    count = 0
                    # Llamar a la función turns del controlador para procesar el movimiento
                    result, movements, subTurn, turn = controller.turns(
                        copy.deepcopy(matrix), m1, m2, turn, subTurn, movements, depth=3
                    )
                    print(result)
                    if result:
                        matrix = result
        # Turno de la IA (jugador 2)
        if turn == 2:
            time.sleep(
                0.5
            )  # Introducir un pequeño retraso antes del movimiento de la IA (opcional)
            # Llamar a la función turns del controlador para que la IA realice su movimiento
            result, movements, subTurn, turn = controller.turns(
                copy.deepcopy(matrix), None, None, turn, subTurn, movements
            )
            print(result)
            if result:
                matrix = result

        if event.type == pygame.USEREVENT:
            # Restaura el botón a su estado normal
            button_pressed = False
            button_save_pressed = False

    # Dibuja la superficie degradada en blank_surface con un modo de mezcla
    blank_surface.fill((0, 0, 0))
    blank_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Dibujar la matriz de imágenes
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            x = col * cell_width
            y = row * cell_height
            cell_value = matrix[row][col]
            image = image_dict.get(cell_value, None)

            if image:
                # Escalar la imagen al tamaño de la celda
                image = pygame.transform.scale(image, (cell_width, cell_height))
                screen.blit(image, (x, y))

            # Dibujar divisiones
            # pygame.draw.rect(screen, (0, 128, 0), (x, y, cell_width, cell_height), 1)

    if button_pressed:
        blank_surface.blit(button_pressed_image, button_rect)
    else:
        blank_surface.blit(button_unpressed_image, button_rect)

    if button_save_pressed:
        blank_surface.blit(button_save_pressed_image, button_save_rect)
    else:
        blank_surface.blit(button_save_unpressed_image, button_save_rect)

    # Renderizar el texto centrado en el rectángulo del texto
    text1 = large_font.render("Linja", True, (0, 0, 0))
    text2 = font.render("Load a Game", True, (0, 0, 0))
    text3 = font.render("Estrategic game", True, (0, 0, 0))
    text_save = font.render("Save game", True, (0, 0, 0))
    blank_surface.blit(text1, text_rect.move(25, 10))
    blank_surface.blit(text2, text_rect.move(18, 100))
    blank_surface.blit(text3, text_rect.move(-5, 50))
    blank_surface.blit(text_save, text_rect.move(27, 245))

    # Pruebas de muestra
    # text4 = font.render("Ganador: IA", True, (0, 0, 0))
    # blank_surface.blit(text4, text_rect.move(18, 300))

    # Llamamos a la función de calcular puntajes
    red_score, black_score, winner = controller.calculate_scores(matrix)
    winner_label = ""

    # Bucle para cambiar el ganador (int) a string entendible por el usuario
    if winner == 1:
        winner_label = "Red"
    else:
        winner_label = "Black"

    # Renderizar textos fuera del bucle de eventos
    text_winner = font.render(f"Winner: {winner_label}", True, (0, 0, 0))
    blank_surface.blit(text_winner, (18, 450))

    text_red_score = font.render(f"Red: {red_score}", True, (0, 0, 0))
    blank_surface.blit(text_red_score, (18, 500))

    text_black_score = font.render(f"Black: {black_score}", True, (0, 0, 0))
    blank_surface.blit(text_black_score, (18, 550))

    # text5 = font.render("Puntaje: 33", True, (0, 0, 0))
    # blank_surface.blit(text5, text_rect.move(18, 320))

    screen.blit(blank_surface, (desired_game_width, 0))  # El área de la derecha.
    pygame.display.flip()


# Salir de Pygame
pygame.quit()
sys.exit()
