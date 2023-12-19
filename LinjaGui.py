import pygame
import sys
from tkinter import Tk, filedialog
import LinjaController as controller
# Inicializar Pygame
pygame.init()


"""
Convenciones del tablero:

0 = Espacios de movimiento
1 = Fichas Rojas
2 = Fichas negras
"""

#Variables
m1 = [0, 0]
m2 = [0, 0]
count = 0
turn = 1
subTurn = 1

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

    matrix = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                row = [int(cell) for cell in line.split()]
                matrix.append(row)
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

# Tamaño de la ventana
matrix_rows = len(matrix)
matrix_cols = len(matrix[0])

# Ancho de la ventana
window_width = 800
# Ancho deseado para el juego
desired_game_width = 600

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
two_button_rect = pygame.Rect(
    600, 200, 160, 80
)  #  Puedes ajustar las coordenadas y el tamaño según tus necesidades


text_rect = pygame.Rect(
    20, 50, 160, 40
)  # Ajusta las coordenadas y el tamaño según tus necesidades

# Cargar las imágenes del botón
button_unpressed_image = pygame.image.load("Sprites/Play_Unpressed.png")
button_pressed_image = pygame.image.load("Sprites/Play_Pressed.png")

# Escalar las imágenes al tamaño deseado (ancho, alto)
button_unpressed_image = pygame.transform.scale(button_unpressed_image, (160, 80))
button_pressed_image = pygame.transform.scale(button_pressed_image, (160, 80))

# Coordenadas donde dibujar la imagen del botón
button_rect = button_unpressed_image.get_rect()
button_rect.topleft = (20, 180)  # Ajusta las coordenadas según tus necesidades

# Estado actual del botón
button_pressed = False

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
    0: pygame.image.load("Sprites\Vacio.png"),
    1: pygame.image.load("Sprites\Ficharoja.png"),
    2: pygame.image.load("Sprites\FichaNegra.png"),
}

# Crear la ventana
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Linja - Juego de Estrategia")


# Bucle principal para la interfaz gráfica
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if two_button_rect.collidepoint(event.pos):
                #cargar_archivo()
                # Cambia el estado del botón
                button_pressed = True
                # Espera un tiempo antes de restaurar el botón a su estado normal
                pygame.time.set_timer(
                    pygame.USEREVENT, 200
                )  # 200 ms (ajusta según tu preferencia)
            else:
                # Obtener las coordenadas al hacer clic en una celda
                row, col = obtener_coordenadas(event.pos)
                print(f"Coordenadas: [{row},{col}] = {matrix[row][col]}")

                if count == 0 and controller.ruleOnlyMoveYourPeace(matrix[row][col], turn):
                    m1 = [row, col]
                    count = 1
                elif count > 0:
                    m2 = [row, col]
                    count = 0
                    result = controller.move(matrix, m1, m2, turn)
                    if result:
                        matrix = result
                    else:
                        print("posicion erronea")

        if event.type == pygame.USEREVENT:
            # Restaura el botón a su estado normal
            button_pressed = False

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

    # Renderizar el texto centrado en el rectángulo del texto
    text1 = large_font.render("Linja", True, (0, 0, 0))
    text3 = font.render("Estrategic game", True, (0, 0, 0))
    blank_surface.blit(text1, text_rect.move(25, 10))
    blank_surface.blit(text3, text_rect.move(1, 40))

    screen.blit(blank_surface, (desired_game_width, 0))  # El área de la derecha.
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
