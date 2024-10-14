import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 450
ALTO = 650
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carrito")

# Colores
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
AZUL_CLARO = (0, 191, 255)

# Frames por segundo
FPS = 60

# Parámetros de la carretera
ancho_linea = 10
alto_linea = 40
espacio_linea = 30  # Espacio entre las líneas
velocidad_linea = 5  # Velocidad del movimiento de las líneas
posiciones_linea = [i * (alto_linea + espacio_linea) for i in range(ALTO // (alto_linea + espacio_linea) + 2)]

# Cargar imágenes del carrito
imagen_carrito = pygame.image.load("player.png")
imagen_carrito = pygame.transform.scale(imagen_carrito, (50, 80))

# Cargar múltiples imágenes para los enemigos
imagenes_enemigos = [
    pygame.transform.scale(pygame.image.load("car1.png"), (50, 80)),
    pygame.transform.scale(pygame.image.load("car2.png"), (50, 80)),
]

# Cargar imágenes de fondo
fondo_menu = pygame.image.load("fondo1.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

fondo_game_over = pygame.image.load("fondo.jpg")
fondo_game_over = pygame.transform.scale(fondo_game_over, (ANCHO, ALTO))

# Definir el jugador
ancho_jugador = 50
alto_jugador = 80
jugador_x = ANCHO // 2 - ancho_jugador // 2
jugador_y = ALTO - alto_jugador - 10
velocidad_jugador = 5

# Definir enemigos
ancho_enemigo = 50
alto_enemigo = 80
velocidad_enemigo = 5
enemigos = []

# Función para comprobar si un enemigo está demasiado cerca de los otros
def esta_cerca(x, y, enemigos):
    for enemigo in enemigos:
        distancia_x = abs(enemigo[0] - x)
        distancia_y = abs(enemigo[1] - y)
        if distancia_x < ancho_enemigo and distancia_y < alto_enemigo:
            return True
    return False

# Función para generar un enemigo con apariencia aleatoria, sin que se sobreponga
def generar_enemigo():
    x = random.randint(0, ANCHO - ancho_enemigo)
    y = random.randint(-100, -40)
    
    # Verificar que el nuevo enemigo no se sobreponga con otros
    while esta_cerca(x, y, enemigos):
        x = random.randint(0, ANCHO - ancho_enemigo)
        y = random.randint(-100, -40)

    imagen_enemigo = random.choice(imagenes_enemigos)  # Seleccionar una imagen aleatoria
    enemigos.append([x, y, imagen_enemigo])

# Función para mover enemigos
def mover_enemigos():
    for enemigo in enemigos:
        enemigo[1] += velocidad_enemigo
        if enemigo[1] > ALTO:
            enemigos.remove(enemigo)

# Función para dibujar al jugador
def dibujar_jugador(x, y):
    ventana.blit(imagen_carrito, (x, y))

# Función para dibujar enemigos
def dibujar_enemigos():
    for enemigo in enemigos:
        ventana.blit(enemigo[2], (enemigo[0], enemigo[1]))  # enemigo[2] es la imagen

# Función para detectar colisiones
def detectar_colision(jugador_x, jugador_y, enemigos):
    for enemigo in enemigos:
        if (enemigo[0] < jugador_x < enemigo[0] + ancho_enemigo or
            enemigo[0] < jugador_x + ancho_jugador < enemigo[0] + ancho_enemigo):
            if (enemigo[1] < jugador_y < enemigo[1] + alto_enemigo or
                enemigo[1] < jugador_y + alto_jugador < enemigo[1] + alto_enemigo):
                return True
    return False

# Función para mover y dibujar las líneas de la carretera
def dibujar_lineas_carretera():
    global posiciones_linea
    for i in range(len(posiciones_linea)):
        pygame.draw.rect(ventana, AMARILLO, (ANCHO // 2 - ancho_linea // 2, posiciones_linea[i], ancho_linea, alto_linea))
        posiciones_linea[i] += velocidad_linea
        if posiciones_linea[i] > ALTO:
            posiciones_linea[i] = -alto_linea

# Función para mostrar el mensaje de "Game Over"
def mostrar_game_over():
    ventana.blit(fondo_game_over, (0, 0))  # Mostrar fondo de Game Over
    fuente = pygame.font.Font(None, 72)
    texto_game_over = fuente.render("GAME OVER", True, ROJO)
    ventana.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 100))

    fuente_pequena = pygame.font.Font(None, 48)
    texto_reiniciar = fuente_pequena.render("Haz clic en REINICIAR", True, BLANCO)
    ventana.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 50))

# Función para crear y manejar el botón de reinicio
def crear_boton_reiniciar():
    fuente_boton = pygame.font.Font(None, 48)
    texto_boton = fuente_boton.render("REINICIAR", True, BLANCO)
    boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 150, 200, 50)

    # Estilo del botón
    pygame.draw.rect(ventana, NEGRO, boton_rect, border_radius=15)  # Borde redondeado
    pygame.draw.rect(ventana, AZUL_CLARO, boton_rect.inflate(-10, -10))  # Borde interior
    ventana.blit(texto_boton, (ANCHO // 2 - texto_boton.get_width() // 2, ALTO // 2 + 150))

    return boton_rect

# Función para mostrar el menú principal
def mostrar_menu_principal():
    ventana.blit(fondo_menu, (0, 0))  # Mostrar fondo del menú
    fuente = pygame.font.Font(None, 72)
    texto_menu = fuente.render("MENÚ PRINCIPAL", True, BLANCO)
    ventana.blit(texto_menu, (ANCHO // 2 - texto_menu.get_width() // 2, ALTO // 2 - 100))

    fuente_boton = pygame.font.Font(None, 48)
    texto_iniciar = fuente_boton.render("INICIAR JUEGO", True, BLANCO)
    boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50)

    # Estilo del botón
    pygame.draw.rect(ventana, NEGRO, boton_rect, border_radius=15)  # Borde redondeado
    pygame.draw.rect(ventana, AZUL_CLARO, boton_rect.inflate(-10, -10))  # Borde interior
    ventana.blit(texto_iniciar, (ANCHO // 2 - texto_iniciar.get_width() // 2, ALTO // 2 + 50))

    return boton_rect

# Función principal del juego
def juego():
    jugando = True
    reloj = pygame.time.Clock()
    puntaje = 0
    global jugador_x, jugador_y, enemigos
    jugador_x = ANCHO // 2 - ancho_jugador // 2
    jugador_y = ALTO - alto_jugador - 10
    enemigos = []

    while jugando:
        reloj.tick(FPS)

        # Dibujar la carretera (fondo gris)
        ventana.fill(GRIS)

        # Dibujar las líneas de la carretera
        dibujar_lineas_carretera()

        # Manejar eventos del teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Eventos de teclado para mover el carrito
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x > 0:
            jugador_x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - ancho_jugador:
            jugador_x += velocidad_jugador
        if teclas[pygame.K_UP] and jugador_y > 0:  # Mover hacia arriba
            jugador_y -= velocidad_jugador
        if teclas[pygame.K_DOWN] and jugador_y < ALTO - alto_jugador:  # Mover hacia abajo
            jugador_y += velocidad_jugador

        # Generar enemigos
        if random.randint(1, 30) == 1:
            generar_enemigo()

        # Mover y dibujar enemigos
        mover_enemigos()
        dibujar_enemigos()

        # Dibujar al jugador
        dibujar_jugador(jugador_x, jugador_y)

        # Verificar colisiones
        if detectar_colision(jugador_x, jugador_y, enemigos):
            jugando = False

        # Actualizar puntaje
        puntaje += 1
        fuente_puntaje = pygame.font.SysFont(None, 36)
        texto_puntaje = fuente_puntaje.render("Puntaje: " + str(puntaje), True, BLANCO)
        ventana.blit(texto_puntaje, (10, 10))

        # Actualizar pantalla
        pygame.display.update()

    # Fin del juego
    game_over()

# Función de Game Over
def game_over():
    global enemigos
    enemigos = []  # Limpiar enemigos
    while True:
        mostrar_game_over()
        boton_reiniciar = crear_boton_reiniciar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                    if boton_reiniciar.collidepoint(evento.pos):
                        juego()  # Reiniciar el juego

        pygame.display.update()

# Iniciar el menú principal
def main():
    while True:
        boton_jugar = mostrar_menu_principal()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                    if boton_jugar.collidepoint(evento.pos):
                        juego()  # Iniciar el juego

        pygame.display.update()

# Llamar a la función principal para comenzar el juego
main()

pygame.quit()
