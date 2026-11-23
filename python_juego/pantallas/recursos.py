# pantallas/recursos.py
# Funciones para cargar imágenes y dibujar el cielo. Las usan varias pantallas.
import os
from PIL import Image, ImageTk

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(BASE, "assets", "imagenes")

_cache = {}     # guarda las imágenes ya cargadas (también evita que Tkinter las borre)


def cargar_imagen(nombre, ancho=None, alto=None, opacidad=1.0):
    """Carga un PNG de assets/imagenes/ y lo achica para que quepa en ancho×alto
    SIN deformarlo. 'opacidad' menor que 1 la hace más transparente (personaje apagado).
    Devuelve None si el archivo no existe."""
    clave = (nombre, ancho, alto, opacidad)
    if clave in _cache:
        return _cache[clave]
    ruta = os.path.join(CARPETA, nombre)
    if not os.path.exists(ruta):
        return None

    imagen = Image.open(ruta).convert("RGBA")
    escalas = []
    if ancho is not None:
        escalas.append(ancho / imagen.width)
    if alto is not None:
        escalas.append(alto / imagen.height)
    if len(escalas) > 0:
        escala = min(escalas)
        imagen = imagen.resize((max(1, int(imagen.width * escala)),
                                max(1, int(imagen.height * escala))), Image.LANCZOS)
    if opacidad < 1.0:
        canal = imagen.getchannel("A").point(lambda v: int(v * opacidad))
        imagen.putalpha(canal)
    foto = ImageTk.PhotoImage(imagen)
    _cache[clave] = foto
    return foto


def cargar_imagen_exacta(nombre, ancho, alto):
    """Carga una imagen y la ajusta EXACTAMENTE a ancho×alto (para pantallas completas)."""
    clave = (nombre, "exacta", ancho, alto)
    if clave in _cache:
        return _cache[clave]
    ruta = os.path.join(CARPETA, nombre)
    if not os.path.exists(ruta):
        return None
    imagen = Image.open(ruta).convert("RGBA").resize((ancho, alto), Image.LANCZOS)
    foto = ImageTk.PhotoImage(imagen)
    _cache[clave] = foto
    return foto


def tamano_imagen(nombre, ancho=None, alto=None):
    """Devuelve (ancho, alto) de la imagen ya ajustada, o None si no existe."""
    foto = cargar_imagen(nombre, ancho, alto)
    if foto is None:
        return None
    return (foto.width(), foto.height())


def dibujar_imagen(lienzo, nombre, x, y, ancho=None, alto=None, placeholder=True,
                   opacidad=1.0, tags=""):
    """Dibuja la imagen centrada en (x, y) y devuelve su id. Si el archivo no existe y
    placeholder=True, dibuja un recuadro avisando qué archivo falta (así el juego no se rompe)."""
    foto = cargar_imagen(nombre, ancho, alto, opacidad)
    if foto is not None:
        return lienzo.create_image(x, y, image=foto, tags=tags)
    if placeholder:
        w = ancho if ancho is not None else 200
        h = alto if alto is not None else 200
        id_recuadro = lienzo.create_rectangle(x - w // 2, y - h // 2, x + w // 2, y + h // 2,
                                              fill="#FDEBD0", outline="#8B5A2B", width=3,
                                              dash=(6, 4), tags=tags)
        lienzo.create_text(x, y, text="Falta\n" + nombre, fill="#8B5A2B",
                           font=("Comic Sans MS", 12, "bold"), justify="center", tags=tags)
        return id_recuadro
    return None


def dibujar_cielo(lienzo, ancho, alto):
    """Cielo azul con degradado: más oscuro arriba y más claro abajo."""
    for fila in range(alto):
        t = fila / alto                       # 0 arriba, 1 abajo
        rojo = int(74 + (143 - 74) * t)
        verde = int(152 + (216 - 152) * t)
        azul = int(232 + (240 - 232) * t)
        color = "#%02x%02x%02x" % (rojo, verde, azul)
        lienzo.create_line(0, fila, ancho, fila, fill=color)
    # Nubes decorativas (si existe casilla_nube.png)
    dibujar_imagen(lienzo, "casilla_nube.png", 120, 90, 170, 130, placeholder=False)
    dibujar_imagen(lienzo, "casilla_nube.png", 990, 70, 200, 150, placeholder=False)
    dibujar_imagen(lienzo, "casilla_nube.png", 60, 560, 220, 160, placeholder=False)
    dibujar_imagen(lienzo, "casilla_nube.png", 1040, 585, 180, 130, placeholder=False)
