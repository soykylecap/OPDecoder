from OP_utils import *
import pygame


# Juevo 1:
inicia_numeros = (
    5, None, None, None, None, 
    None, None, None, None, None, 
    None, None, None, None, None, 
    None, None, None, None, None, 
    None, None, None, None, 1
    )
topes_derecha = (
    False, False, False, False, True, 
    True, False, True, False, True, 
    False, False, False, False, True, 
    False, True, False, False, True, 
    False, False, False, False, True
    )
topes_abajo = (
    False, False, True, False, False,
    False, False, False, True, False,
    False, False, True, False, False,
    False, False, False, False, False,
    True, True, True, True, True
    )


# # Juego 2:
# inicia_numeros = (
#     None, 5, None, None, None, None, 
#     None, None, None, 5, None, None, 
#     None, None, 1, None, None, None, 
#     None, None, None, None, None, None,
#     None, None, None, None, None, None, 
#     None, None, None, None, None, None
# )

# topes_derecha = (
#     False, False, False, False, False, True,
#     False, False, False, False, False, True,
#     False, False, False, False, True, True,
#     False, False, True, False, False, True,
#     False, False, False, True, False, True,
#     False, False, False, False, False, True
# )

# topes_abajo = (
#     False, False, False, False, False, False, 
#     False, False, False, False, False, False, 
#     False, False, True, False, False, False, 
#     True, False, False, False, False, False, 
#     False, False, False, False, True, False, 
#     True, True, True, True, True, True, 
#     )


# # Juego 3:
# inicia_numeros = (
#     None, None, None, None, None,
#     None, None, None, None, None, 
#     4, 3, None, None, None, 
#     None, None, None, None, None, 
#     None, None, None, None, None,
#     )

# topes_derecha = (
#     False, False, False, False, True, 
#     True, False, True, False, True,
#     False, False, False, False, True,
#     False, False, True, False, True, 
#     False, False, False, False, True
#     )

# topes_abajo = (
#     False, False, False, False, False,
#     False, False, False, True, False,
#     False, False, True, False, False,
#     False, False, False, True, False,
#     True, True, True, True, True,
#     )


# Juego 4:
# inicia_numeros = (
#     None, None, None, None, 6, None, None,
#     None, None, None, None, None, None, 3,
#     None, None, None, None, None, None, None,
#     None, None, None, None, None, None, 1,
#     None, None, 2, None, None, 3, None,
#     None, None, None, None, None, None, None,
#     None, None, None, None, None, None, None,
#     )

# topes_derecha = (
#     False, False, False, False, False, False, True,
#     False, False, False, True, False, False, True,
#     False, False, True, False, False, False, True,
#     False, False, False, False, False, False, True,
#     False, False, False, False, False, False, True,
#     False, False, False, True, False, False, True,
#     False, True, False, False, False, False, True,
#     )

# topes_abajo = (
#     False, False, False, False, False, False, False,
#     True, False, False, False, False, False, False,
#     False, False, True, False, False, True, False,
#     False, True, False, False, False, False, False,
#     False, False, False, False, False, False, False,
#     False, False, False, False, False, False, False,
#     True, True, True, True, True, True, True,
#     )


tablero = Tablero(int(math.sqrt(len(inicia_numeros))), topes_abajo, topes_derecha, inicia_numeros)
tablero.configurar_celdas()
resolver(2, tablero)





#Inicializar pygame
pygame.init()

#Configurar la pantalla
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Up Puzzle Decoder")


#Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 87, 51)
GRAY = (200, 200, 200)

#Tamaño de las celdas
CELL_SIZE = WIDTH // tablero.maximo


# Dibujar la cuadrícula
def draw_grid():
    # Dibujar lineas
    for i in range(tablero.maximo):
        width = 1
        #Líneas horizontales
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)
        #Líneas verticales
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), width)
    
    # Agrega lineas gruesas
    for celda_actual in tablero.celdas:
        if celda_actual.final_abajo:
            pygame.draw.line(screen, BLACK, ((celda_actual.columna - 1) * CELL_SIZE, celda_actual.fila * CELL_SIZE), (celda_actual.columna * CELL_SIZE, celda_actual.fila * CELL_SIZE), 6)
        if celda_actual.final_derecha:
            pygame.draw.line(screen, BLACK, (celda_actual.columna * CELL_SIZE, (celda_actual.fila - 1) * CELL_SIZE), (celda_actual.columna * CELL_SIZE, celda_actual.fila * CELL_SIZE), 6)
    
    # Dibujar números en cada celda
    
    
    for celda_actual in tablero.celdas:
        font = pygame.font.Font(None, 40)  # Fuente para los números
        if celda_actual.numero_inicio is not None:
            # Calcular posición del texto en el centro de la celda
            font.italic = True
            text = font.render(str(celda_actual.numero_inicio), True, RED)
            text_rect = text.get_rect(
                center=((celda_actual.columna - 0.5) * CELL_SIZE, (celda_actual.fila - 0.5) * CELL_SIZE)
            )
            screen.blit(text, text_rect)
        elif celda_actual.numero is not None:
            # Calcular posición del texto en el centro de la celda
            font.italic = False
            text = font.render(str(celda_actual.numero), True, BLACK)
            text_rect = text.get_rect(
                center=((celda_actual.columna - 0.5) * CELL_SIZE, (celda_actual.fila - 0.5) * CELL_SIZE)
            )
            screen.blit(text, text_rect)
       # El siguiente else muestra los maximos posibles en las celdas vacias.
        else:
            font = pygame.font.Font(None, 15)
            font.italic = False
            text = font.render(str(celda_actual.candidatos), True, GRAY)
            text_rect = text.get_rect(
                center=((celda_actual.columna - 0.5) * CELL_SIZE, (celda_actual.fila - 0.5) * CELL_SIZE)
            )
            screen.blit(text, text_rect)

#Main loop
def main():
    running = True
    while running:
        screen.fill(WHITE)
        
        #Dibujar la cuadrícula
        draw_grid()

        #Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        #Actualizar pantalla
        pygame.display.flip()


            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()















