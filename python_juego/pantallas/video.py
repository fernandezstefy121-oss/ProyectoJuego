# pantallas/video.py
# Fondo en movimiento. Tkinter no reproduce vídeo, así que el vídeo se guardó como una
# secuencia de imágenes (assets/video/partida/frame_0000.jpg, frame_0001.jpg, ...)
# y aquí se muestran una tras otra, en bucle, con after() para no congelar la ventana.
import glob
import os
from PIL import Image, ImageTk

from pantallas.recursos import dibujar_cielo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(BASE, "assets", "video", "partida")
FPS = 16


def crear_fondo(lienzo, ventana, ancho, alto):
    """Prepara el fondo en el lienzo y devuelve un 'controlador' (diccionario).
    Si no hay cuadros del vídeo, dibuja un cielo fijo para que el juego funcione igual."""
    cuadros = sorted(glob.glob(os.path.join(CARPETA, "frame_*.jpg")))
    control = {"cuadros": cuadros, "i": 0, "activo": False, "item": None,
               "foto": None, "lienzo": lienzo, "ventana": ventana, "id_after": None}
    if len(cuadros) == 0:
        dibujar_cielo(lienzo, ancho, alto)
    else:
        control["item"] = lienzo.create_image(0, 0, anchor="nw")
    return control


def iniciar(control):
    """Empieza (o sigue) reproduciendo el vídeo en bucle."""
    if len(control["cuadros"]) == 0 or control["activo"]:
        return
    control["activo"] = True
    siguiente_cuadro(control)


def detener(control):
    """Pausa el vídeo (se usa al salir de la pantalla para no gastar recursos)."""
    control["activo"] = False
    if control["id_after"] is not None:
        try:
            control["ventana"].after_cancel(control["id_after"])
        except Exception:
            pass
        control["id_after"] = None


def siguiente_cuadro(control):
    if not control["activo"]:
        return
    try:
        imagen = Image.open(control["cuadros"][control["i"]])
        foto = ImageTk.PhotoImage(imagen)
        imagen.close()
        control["lienzo"].itemconfig(control["item"], image=foto)
        control["foto"] = foto               # se guarda para que Tkinter no la borre
    except Exception:
        pass                                 # si falla un cuadro, se salta
    control["i"] = (control["i"] + 1) % len(control["cuadros"])
    control["id_after"] = control["ventana"].after(int(1000 / FPS),
                                                   lambda: siguiente_cuadro(control))
