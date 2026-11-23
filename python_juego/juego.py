# juego.py - Reglas del Tres en Raya escritas como funciones.
# Son las MISMAS reglas de logica.py (turno con jugadas % 2, pila con append/pop,
# victoria con recorridos [0..2] por filas, columnas y diagonales).
# Aquí solo están ordenadas en funciones para que la interfaz gráfica las pueda usar.
import os
from datetime import date

CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA, "historial.csv")
ENCABEZADO = "id_partida,jugador_x,jugador_o,resultado,fecha\n"

tablero = [["", "", ""],
           ["", "", ""],
           ["", "", ""]]
jugadas = 0
pila = []


def nuevo_juego():
    """Vacía el tablero y reinicia las jugadas y la pila."""
    global jugadas
    for i in range(3):
        for j in range(3):
            tablero[i][j] = ""
    jugadas = 0
    pila.clear()


def turno_actual():
    """Devuelve "X" o "O" según jugadas % 2."""
    if jugadas % 2 == 0:
        return "X"
    else:
        return "O"


def poner_ficha(fila, columna):
    """Pone la ficha del turno actual. Devuelve "fuera", "ocupada" o "ok"."""
    global jugadas
    if fila < 0 or fila > 2 or columna < 0 or columna > 2:
        return "fuera"
    if tablero[fila][columna] != "":
        return "ocupada"
    turno = turno_actual()
    tablero[fila][columna] = turno
    jugadas = jugadas + 1
    pila.append([fila, columna, turno])
    return "ok"


def linea_ganadora(turno):
    """Si 'turno' tiene tres en raya, devuelve las 3 casillas [(fila, col), ...].
    Si no, devuelve una lista vacía."""
    # Revisar las 3 filas
    for i in range(3):
        if tablero[i][0] == turno and tablero[i][1] == turno and tablero[i][2] == turno:
            return [(i, 0), (i, 1), (i, 2)]

    # Revisar las 3 columnas
    for j in range(3):
        if tablero[0][j] == turno and tablero[1][j] == turno and tablero[2][j] == turno:
            return [(0, j), (1, j), (2, j)]

    # Diagonal principal: (0,0) (1,1) (2,2)
    if tablero[0][0] == turno and tablero[1][1] == turno and tablero[2][2] == turno:
        return [(0, 0), (1, 1), (2, 2)]

    # Diagonal secundaria: (0,2) (1,1) (2,0)
    if tablero[0][2] == turno and tablero[1][1] == turno and tablero[2][0] == turno:
        return [(0, 2), (1, 1), (2, 0)]

    return []


def hay_ganador(turno):
    """True si 'turno' ganó."""
    return len(linea_ganadora(turno)) > 0


def deshacer():
    """Quita la última jugada con pop(). Devuelve [fila, col, turno] o None si no hay nada."""
    global jugadas
    if len(pila) == 0:
        return None
    ultima = pila.pop()
    tablero[ultima[0]][ultima[1]] = ""
    jugadas = jugadas - 1
    return ultima


def guardar_partida(nombre_x, nombre_o, resultado):
    """Agrega la partida a historial.csv y devuelve su id.
    Si el archivo no existe lo crea con el encabezado."""
    if not os.path.exists(RUTA_CSV):
        archivo = open(RUTA_CSV, "w", encoding="utf-8")
        archivo.write(ENCABEZADO)
        archivo.close()

    archivo = open(RUTA_CSV, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()

    # El id es el número de líneas con datos (la 1ª línea es el encabezado)
    con_datos = 0
    for linea in lineas:
        if linea.strip() != "":
            con_datos = con_datos + 1
    id_partida = con_datos

    archivo = open(RUTA_CSV, "a", encoding="utf-8")
    # Si la última línea no termina en salto de línea, se agrega (evita líneas pegadas)
    if len(lineas) > 0 and not lineas[-1].endswith("\n"):
        archivo.write("\n")
    archivo.write(str(id_partida) + "," + nombre_x + "," + nombre_o + "," + resultado + "," + str(date.today()) + "\n")
    archivo.close()
    return id_partida
