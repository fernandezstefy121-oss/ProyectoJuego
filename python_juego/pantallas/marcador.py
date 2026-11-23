# pantallas/marcador.py
# Marcador permanente: se guarda en datos/marcador.json y se conserva al cerrar el programa.
# Es independiente de la lógica del juego (juego.py no sabe que existe).
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(BASE, "datos", "marcador.json")

datos = {"snoopy": 0, "baron": 0, "empates": 0}


def cargar():
    """Lee el archivo. Si no existe o está dañado, empieza en cero."""
    global datos
    datos = {"snoopy": 0, "baron": 0, "empates": 0}
    if not os.path.exists(RUTA):
        return
    try:
        archivo = open(RUTA, "r", encoding="utf-8")
        leido = json.load(archivo)
        archivo.close()
        for clave in datos:
            if isinstance(leido.get(clave), int) and leido[clave] >= 0:
                datos[clave] = leido[clave]
    except (OSError, ValueError):
        datos = {"snoopy": 0, "baron": 0, "empates": 0}


def guardar():
    """Escribe el archivo (crea la carpeta datos/ si no existe)."""
    try:
        os.makedirs(os.path.dirname(RUTA), exist_ok=True)
        archivo = open(RUTA, "w", encoding="utf-8")
        json.dump(datos, archivo, indent=2)
        archivo.close()
    except OSError:
        pass        # si no se puede guardar, el juego sigue funcionando


def sumar_resultado(resultado):
    """resultado: "X" (gana Snoopy), "O" (gana el Barón Rojo) o "EMPATE"."""
    if resultado == "X":
        datos["snoopy"] = datos["snoopy"] + 1
    elif resultado == "O":
        datos["baron"] = datos["baron"] + 1
    else:
        datos["empates"] = datos["empates"] + 1
    guardar()


cargar()
