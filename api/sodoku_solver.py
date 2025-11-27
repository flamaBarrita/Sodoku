# Lista global donde guardaremos cada paso para la animación
historial_visual = []

def tomar_foto(tablero):
    """
    Saca una copia instantánea del tablero en su estado actual
    y la guarda en el historial para enviarla al Frontend.
    """
    # Creamos una copia exacta (profunda) fila por fila
    copia = [fila[:] for fila in tablero]
    historial_visual.append(copia)

def buscar_casilla_vacia(tablero, coordenadas):
    """
    Busca un '0' en el tablero. 
    Si lo encuentra, guarda la posición en la lista 'coordenadas' [fila, col] 
    y devuelve True. Si no hay ceros, devuelve False (tablero lleno).
    """
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                # Modificamos la lista 'coordenadas' que nos pasaron por referencia
                coordenadas[0] = fila
                coordenadas[1] = col
                return True
    return False

def es_movimiento_seguro(tablero, fila, col, numero):
    """
    Verifica si poner el numero en tablero[fila][col] rompe alguna regla.
    """
    #fila horizontal
    for i in range(9):
        if tablero[fila][i] == numero:
            return False
            
    #columna vertical
    for i in range(9):
        if tablero[i][col] == numero:
            return False
            
    #regla del CUADRANTE 3x3
    inicio_fila = fila - (fila % 3)
    inicio_col = col - (col % 3)
    
    for i in range(3):
        for j in range(3):
            if tablero[i + inicio_fila][j + inicio_col] == numero:
                return False
                
    return True

def resolver_sudoku(tablero):
    #algoritmo principal de backtracking
    # Variable auxiliar para guardar [fila, columna] de la casilla vacía
    coordenadas = [0, 0] 

    # caso base si no hay casillas vacías, hemos terminado
    if not buscar_casilla_vacia(tablero, coordenadas):
        return True

    # Extraemos la posición que encontró la función de arriba
    fila = coordenadas[0]
    col = coordenadas[1]

    # Intentamos probar números del 1 al 9
    for numero in range(1, 10):
        
        if es_movimiento_seguro(tablero, fila, col, numero):
            
            # Ponemos el número
            tablero[fila][col] = numero
            tomar_foto(tablero) # tomamos foto tras poner el número
 
            # Intentamos resolver el resto del tablero
            if resolver_sudoku(tablero):
                return True # éxito en la recursión

            # becktracking:
            # Si el camino no funcionó, borramos el número (volvemos a 0)
            # y probamos con el siguiente del bucle for.
            tablero[fila][col] = 0
            tomar_foto(tablero) #se borra el numero pero tomamos foto igualmente

    # Si probamos del 1 al 9 y nada funcionó, este camino no sirve.
    return False