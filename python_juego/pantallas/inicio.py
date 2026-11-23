# pantallas/inicio.py - Pantalla principal (menú)
import os
import tkinter as tk
from PIL import Image, ImageTk          # Pillow: para abrir y escalar imágenes

from pantallas import sonidos
from pantallas.botones import crear_boton

# Carpeta del proyecto (python_juego/), sin importar desde dónde se ejecute
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FONDO = os.path.join(BASE, "assets", "imagenes", "fondo_inicio.jpg")
RUTA_PANTALLA = os.path.join(BASE, "assets", "imagenes", "pantalla_inicio.jpg")   # el diseño completo

# Zonas de clic sobre los botones dibujados en pantalla_inicio.jpg (ya ajustadas a 1100×650)
# Cada zona: (x1, y1, x2, y2, nombre)
ZONAS = [(706, 353, 1043, 444, "jugar"),
         (733, 446, 1046, 508, "sonido"),
         (733, 512, 1041, 586, "salir")]

COLOR_BORDE_TITULO = "#123A6B"


def cargar_fondo(ruta, ancho, alto):
    """Abre la imagen y la ajusta a la ventana SIN deformarla:
    la agranda hasta cubrir todo y recorta lo que sobra del centro."""
    imagen = Image.open(ruta).convert("RGB")
    escala = max(ancho / imagen.width, alto / imagen.height)
    nuevo_ancho = int(imagen.width * escala) + 1
    nuevo_alto = int(imagen.height * escala) + 1
    imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    izquierda = (nuevo_ancho - ancho) // 2
    arriba = (nuevo_alto - alto) // 2
    imagen = imagen.crop((izquierda, arriba, izquierda + ancho, arriba + alto))
    return ImageTk.PhotoImage(imagen)


def cargar_imagen_exacta(ruta, ancho, alto):
    """Abre la imagen y la estira a ancho×alto (para el diseño completo de la pantalla)."""
    imagen = Image.open(ruta).convert("RGB")
    imagen = imagen.resize((ancho, alto), Image.LANCZOS)
    return ImageTk.PhotoImage(imagen)


def crear_pantalla_con_diseno(marco, ventana, ir_a, ancho, alto):
    """Pantalla de inicio usando tu diseño completo (pantalla_inicio.jpg).
    Los botones ya están dibujados en la imagen, así que se ponen zonas de clic encima."""
    lienzo = tk.Canvas(marco, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack()
    foto = cargar_imagen_exacta(RUTA_PANTALLA, ancho, alto)
    lienzo.create_image(0, 0, image=foto, anchor="nw")
    lienzo.foto_fondo = foto          # guarda la imagen para que Tkinter no la borre

    def dibujar_estado_sonido():
        """Texto chico bajo los botones que dice si el sonido está activado."""
        lienzo.delete("estado_sonido")
        if sonidos.sonido_activo:
            texto = "SONIDO: SÍ"
        else:
            texto = "SONIDO: NO"
        fuente = ("Comic Sans MS", 14, "bold")
        lienzo.create_text(891, 612, text=texto, font=fuente, fill="#3B2A1A", tags="estado_sonido")
        lienzo.create_text(889, 610, text=texto, font=fuente, fill="white", tags="estado_sonido")

    def zona_en(x, y):
        """Devuelve la zona (tupla) que está bajo el mouse, o None."""
        for z in ZONAS:
            if z[0] <= x <= z[2] and z[1] <= y <= z[3]:
                return z
        return None

    def al_mover(evento):
        lienzo.delete("resaltado")
        z = zona_en(evento.x, evento.y)
        if z is None:
            lienzo.config(cursor="")
        else:
            lienzo.config(cursor="hand2")
            lienzo.create_rectangle(z[0], z[1], z[2], z[3], outline="white", width=3,
                                    tags="resaltado")

    def al_clic(evento):
        z = zona_en(evento.x, evento.y)
        if z is None:
            return
        if z[4] == "jugar":
            ir_a("presentacion")
        elif z[4] == "sonido":
            sonidos.alternar()
            dibujar_estado_sonido()
        elif z[4] == "salir":
            ventana.destroy()         # cierra el programa directamente, sin preguntar

    lienzo.bind("<Motion>", al_mover)
    lienzo.bind("<Button-1>", al_clic)
    dibujar_estado_sonido()


def dibujar_cielo_de_respaldo(lienzo, ancho, alto):
    """Si todavía no está la imagen de fondo, se dibuja un cielo azul con nubes."""
    lienzo.create_rectangle(0, 0, ancho, alto, fill="#4A90D9", outline="")
    nubes = [(150, 120), (520, 80), (900, 160), (300, 480), (800, 520)]
    for nube in nubes:
        x = nube[0]
        y = nube[1]
        lienzo.create_oval(x - 80, y - 25, x + 80, y + 25, fill="white", outline="")
        lienzo.create_oval(x - 40, y - 50, x + 30, y + 10, fill="white", outline="")


def texto_con_borde(lienzo, x, y, texto, tam, color="white", borde=COLOR_BORDE_TITULO, tags=""):
    """Letras con contorno: Tkinter no trae contorno, así que se dibuja el texto
    varias veces en color oscuro, un poco corrido, y encima el texto claro."""
    fuente = ("Comic Sans MS", tam, "bold")
    lienzo.create_text(x + 6, y + 8, text=texto, font=fuente, fill="#0B2A4A", tags=tags)    # sombra
    corrimientos = [(-4, -4), (-4, 0), (-4, 4), (0, -4), (0, 4), (4, -4), (4, 0), (4, 4)]
    for c in corrimientos:
        lienzo.create_text(x + c[0], y + c[1], text=texto, font=fuente, fill=borde, tags=tags)
    lienzo.create_text(x, y, text=texto, font=fuente, fill=color, tags=tags)


def dibujar_cinta(lienzo, cx, cy, texto):
    """Cinta roja con el texto 'VS. BARÓN ROJO'."""
    rojo = "#D62828"
    oscuro = "#8E1B1B"
    # Colas de la cinta (atrás)
    lienzo.create_polygon(cx - 230, cy - 18, cx - 280, cy - 18, cx - 255, cy + 8,
                          cx - 280, cy + 34, cx - 230, cy + 34, fill=oscuro, outline="white", width=3)
    lienzo.create_polygon(cx + 230, cy - 18, cx + 280, cy - 18, cx + 255, cy + 8,
                          cx + 280, cy + 34, cx + 230, cy + 34, fill=oscuro, outline="white", width=3)
    # Cinta principal
    lienzo.create_rectangle(cx - 235, cy - 30, cx + 235, cy + 30, fill=rojo, outline="white", width=4)
    lienzo.create_text(cx, cy, text=texto, fill="white", font=("Comic Sans MS", 26, "bold"))


def crear_pantalla(ventana, ir_a, ancho, alto):
    """Construye la pantalla de inicio y la devuelve (un Frame).
    'ir_a' es la función de main.py que cambia de pantalla."""
    marco = tk.Frame(ventana)

    # Si existe el diseño completo, se usa ese y se termina aquí
    if os.path.exists(RUTA_PANTALLA):
        crear_pantalla_con_diseno(marco, ventana, ir_a, ancho, alto)
        return marco

    # Si no, se usa la versión dibujada con código (fondo + título + botones)
    lienzo = tk.Canvas(marco, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack()

    # ----- Fondo -----
    if os.path.exists(RUTA_FONDO):
        foto = cargar_fondo(RUTA_FONDO, ancho, alto)
        lienzo.create_image(0, 0, image=foto, anchor="nw")
        lienzo.foto_fondo = foto     # ¡importante! guarda la imagen o Tkinter la borra de la memoria
    else:
        dibujar_cielo_de_respaldo(lienzo, ancho, alto)

    # ----- Título (a la derecha, donde el fondo está despejado) -----
    cx = 730
    texto_con_borde(lienzo, cx, 105, "SNOOPY", 72)
    dibujar_cinta(lienzo, cx, 195, "VS. BARÓN ROJO")

    # ----- Botones -----
    def accion_jugar():
        ir_a("presentacion")

    def accion_sonido():
        activo = sonidos.alternar()
        if activo:
            lienzo.itemconfig(id_texto_sonido, text="SONIDO: SÍ")
        else:
            lienzo.itemconfig(id_texto_sonido, text="SONIDO: NO")

    def accion_salir():
        ventana.destroy()            # cierra el programa directamente, sin preguntar

    crear_boton(lienzo, cx, 310, 300, 66, "JUGAR", accion_jugar,
                color="#F39C12", color_hover="#FFB547", tam_letra=26)
    id_texto_sonido = crear_boton(lienzo, cx, 400, 300, 66, "SONIDO: SÍ", accion_sonido,
                                  color="#2E86C1", color_hover="#5DADE2")
    crear_boton(lienzo, cx, 490, 300, 66, "SALIR", accion_salir,
                color="#C0392B", color_hover="#E74C3C")

    return marco
