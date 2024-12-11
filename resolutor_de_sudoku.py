import pygame

# Inicializamos la libreria pygame
pygame.init()

# Configuramos la ventana dandole un tamaño,color y le pones el titulo
tamaño_ventana = 540
altura_total = tamaño_ventana + 90  
tamaño_celda = tamaño_ventana // 9
ventana = pygame.display.set_mode((tamaño_ventana, altura_total))
pygame.display.set_caption("Sudoku Solver")
ventana.fill((150, 200, 150))  # Fondo verde claro

# Tablero inicial vacío (0 representa celdas vacías)
tablero_juego = [[0 for _ in range(9)] for _ in range(9)]  # Generamos un tablero vacío 9x9, el _ indica que no nos importa el valor

# Con esta matriz de booleanos sabemos si el usuario a introducido algun numero
numeros_usuario = [[False for _ in range(9)] for _ in range(9)]

# Marcamos la celda que el usuario seleccione
celda_seleccionada = None

# Con esta función dibujamos el tablero
def pintar_tablero(ventana):
    for i in range(10):  # Como son 9 celdas dibujamos 10 lineas para separarlas
        grosor = 6 if i % 3 == 0 else 2  # Establecemos las lineas gruesas, las negras, cada 3 lineas
        color = (0, 0, 0) if i % 3 == 0 else (200, 0, 0)  # Le damos el color a cada tipo de linea
        # Dibujamos las líneas horizontales del sudoku
        pygame.draw.line(ventana, color, (0, i * tamaño_celda), (tamaño_ventana, i * tamaño_celda), grosor)
        # Dibujamos las líneas verticales
        pygame.draw.line(ventana, color, (i * tamaño_celda, 0), (i * tamaño_celda, tamaño_ventana), grosor)

# Esta funcion nos permite dibujar los numeros en el tablero
def dibujar_numeros(ventana, tablero):
    fuente = pygame.font.SysFont("arial", 30)  # Le damos una fuente y un tamaño a los numeros introducidos por el usuario
    for fila in range(9):
        for columna in range(9):
            valor = tablero[fila][columna]
            if valor != 0:
                x = columna * tamaño_celda + tamaño_celda // 2
                y = fila * tamaño_celda + tamaño_celda // 2
                # Aqui le damos un color al numero dependiendo de si es introducido por el usuario o no
                color = (255, 255, 100) if numeros_usuario[fila][columna] else (0, 0, 0)
                texto = fuente.render(str(valor), True, color) 
                texto_rect = texto.get_rect(center=(x, y))
                ventana.blit(texto, texto_rect)

# Con esta funcion resaltamos con un azul claro la celda que el usuario tiene marcada
def celda_marcada(ventana, fila, columna):
    x = columna * tamaño_celda
    y = fila * tamaño_celda
    pygame.draw.rect(ventana, (173, 216, 230), (x, y, tamaño_celda, tamaño_celda), 5)

# Con esta funcion reiniciamos el tablero en el caso de que el usuario lo requiera
def reiniciar_tablero():
    global tablero_juego, numeros_usuario
    tablero_juego = [[0 for _ in range(9)] for _ in range(9)]  # Volvemos a iniciar el tablero vacio,sin ningun numero
    numeros_usuario = [[False for _ in range(9)] for _ in range(9)]  # Volvemos a establecer todo a False

# Con esta funcion verificamos si el numero es valido
def valido(tablero, fila, columna, numero):
    # Primero verificamos las filas
    for i in range(9):
        if tablero[fila][i] == numero:
            return False
    # Ahora verificamos las columnas
    for i in range(9):
        if tablero[i][columna] == numero:
            return False
    # Por ultimo tenemos que verificar las cuadriculas pequeñas las de 3x3
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_columna + j] == numero:
                return False
    return True

# Con esta funcion resolvemos el sudoku mediante backtracking
def resolver_sudoku(tablero):
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:  
                for numero in range(1, 10):  
                    if valido(tablero, fila, columna, numero):
                        tablero[fila][columna] = numero
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila][columna] = 0  
                return False  
    return True

# Gracias a esta funcion dibujamos los botones en la parte inferior
def dibujar_botones(ventana):
    # Le damos tamaño y direccion a los botones
    ancho_boton = 120
    alto_boton = 40
    x_boton_izquierdo = (tamaño_ventana // 2) - ancho_boton - 50  # Configuramos el boton izquierdo
    x_boton_derecho = (tamaño_ventana // 2) + 50  # Ahora lo hacemos con el derecho
    y_boton = tamaño_ventana + 4  # Le decimos en que lugar los queremos

    # Dibujamos los botones reiniciar y resolver
    pygame.draw.rect(ventana, (173, 216, 230), (x_boton_izquierdo, y_boton, ancho_boton, alto_boton))
    pygame.draw.rect(ventana, (173, 216, 230), (x_boton_derecho, y_boton, ancho_boton, alto_boton))


    # Le damos el nombre a los botones
    fuente = pygame.font.Font(None, 30)
    texto_izquierdo = fuente.render("Reiniciar", True, (0, 0, 0))
    texto_derecho = fuente.render("Resolver", True, (0, 0, 0))
    
    ventana.blit(texto_izquierdo, texto_izquierdo.get_rect(center=(x_boton_izquierdo + ancho_boton // 2, y_boton + alto_boton // 2)))
    ventana.blit(texto_derecho, texto_derecho.get_rect(center=(x_boton_derecho + ancho_boton // 2, y_boton + alto_boton // 2)))

# Con esta funcion sabemos en que celda el usuario a echo un click
def clic_usuario_boton(posicion, x, y, ancho, alto):
    return x <= posicion[0] <= x + ancho and y <= posicion[1] <= y + alto

# Función para mostrar mensajes en la ventana
def mostrar_mensaje(ventana, mensaje,color):
    fuente = pygame.font.Font(None, 40)
    texto = fuente.render(mensaje, True,color)
    ventana.blit(texto, (tamaño_ventana // 2 - texto.get_width() // 2, tamaño_ventana + 50))


# Inicializamos el mensaje antes
mensaje_actual = ""
mensaje_color = (0, 0, 0)  # Establecemos el color negro por defecto

# Establecemos el bucle principal del programa
funcionando = True
while funcionando:
    for accion in pygame.event.get():
        if accion.type == pygame.QUIT:  # Si el usuario le da a la X, cerramos el programa
            funcionando = False
        elif accion.type == pygame.MOUSEBUTTONDOWN:  # Detectamos el clic en el tablero o botones
            posicion = pygame.mouse.get_pos()

            # Tamaño y posición de los botones
            ancho_boton = 120
            alto_boton = 40
            x_boton_izquierdo = (tamaño_ventana // 2) - ancho_boton - 50
            x_boton_derecho = (tamaño_ventana // 2) + 50
            y_boton = tamaño_ventana + 4

            if clic_usuario_boton(posicion, x_boton_izquierdo, y_boton, ancho_boton, alto_boton):
                reiniciar_tablero()
                mensaje_actual = "Tablero reiniciado!"  # Mensaje al reiniciar
                mensaje_color = (0, 51, 102)
            elif clic_usuario_boton(posicion, x_boton_derecho, y_boton, ancho_boton, alto_boton):
                if resolver_sudoku(tablero_juego):
                    mensaje_actual = "El sudoku se ha resuelto!"
                    mensaje_color = (0, 51, 102)
                else:
                    mensaje_actual = "El sudoku no se ha podido resolver!"
                    mensaje_color = (0, 51, 102)

            # Si no es un botón, selecciona la celda
            if posicion[1] < tamaño_celda * 9:
                fila = posicion[1] // tamaño_celda
                columna = posicion[0] // tamaño_celda
                celda_seleccionada = (fila, columna)
        elif accion.type == pygame.KEYDOWN:  # Detectamos la entrada del teclado
            if celda_seleccionada:
                fila, columna = celda_seleccionada
                if accion.unicode.isdigit() and accion.unicode != '0': 
                    tablero_juego[fila][columna] = int(accion.unicode)  
                    numeros_usuario[fila][columna] = True 

    ventana.fill((150, 200, 150))  # Le damos al fondo del sudoku un verde claro
    pintar_tablero(ventana)  # Dibujamos las líneas del tablero
    dibujar_numeros(ventana, tablero_juego)  # Dibujamos los números en las celdas del tablero
    if celda_seleccionada:  # Resaltamos la celda seleccionada
        celda_marcada(ventana, celda_seleccionada[0], celda_seleccionada[1])
    dibujar_botones(ventana)  # Dibujamos los botones
    
    # Mostrar el mensaje actual si existe
    if mensaje_actual:
        mostrar_mensaje(ventana, mensaje_actual, mensaje_color)
    
    pygame.display.update()  # Actualizamos la pantalla

pygame.quit()

