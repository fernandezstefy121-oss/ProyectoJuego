# pantallas/dialogos.py
# Cuadros de confirmación (SÍ / NO) dibujados sobre el lienzo.
# Los botones SÍ y NO ya vienen dentro de la imagen, así que se ponen zonas de clic encima.
from pantallas.recursos import cargar_imagen

# 'tam' es el tamaño original de cada imagen y 'si' / 'no' son las zonas de los botones
# dentro de esa imagen (x1, y1, x2, y2).
DIALOGOS = {
    "reiniciar": {"archivo": "confirmar_reiniciar.png", "tam": (623, 399),
                  "si": (77, 279, 312, 363), "no": (351, 279, 572, 363),
                  "pregunta": "¿Deseas empezar una nueva partida?\nSe perderá la partida actual."},
    "menu": {"archivo": "confirmar_menu_principal.png", "tam": (627, 396),
             "si": (74, 279, 311, 360), "no": (348, 280, 570, 360),
             "pregunta": "¿Deseas regresar al menú principal?"},
    "deshacer": {"archivo": "confirmar_deshacer.png", "tam": (635, 398),
                 "si": (76, 278, 312, 362), "no": (349, 278, 577, 362),
                 "pregunta": "¿Deseas deshacer el último movimiento?"},
}
ANCHO_DIALOGO = 560

actual = None       # datos del cuadro que está abierto (None si no hay ninguno)


def _escalar(zona, escala, x0, y0):
    return (x0 + zona[0] * escala, y0 + zona[1] * escala,
            x0 + zona[2] * escala, y0 + zona[3] * escala)


def mostrar(lienzo, ancho, alto, clave, al_si, al_no=None):
    """Abre el cuadro 'clave'. 'al_si' se ejecuta si presionan SÍ; 'al_no' (opcional) con NO."""
    global actual
    datos = DIALOGOS[clave]
    lienzo.delete("dialogo")
    # Capa oscura para que se note que lo de atrás está bloqueado
    lienzo.create_rectangle(0, 0, ancho, alto, fill="black", stipple="gray50",
                            outline="", tags="dialogo")
    foto = cargar_imagen(datos["archivo"], ANCHO_DIALOGO)
    if foto is not None:
        escala = foto.width() / datos["tam"][0]
        x0 = ancho / 2 - foto.width() / 2
        y0 = alto / 2 - foto.height() / 2
        lienzo.create_image(ancho / 2, alto / 2, image=foto, tags="dialogo")
        zona_si = _escalar(datos["si"], escala, x0, y0)
        zona_no = _escalar(datos["no"], escala, x0, y0)
    else:
        # Respaldo si falta la imagen: cuadro sencillo dibujado con código
        cx = ancho / 2
        cy = alto / 2
        lienzo.create_rectangle(cx - 280, cy - 150, cx + 280, cy + 150, fill="#FFF4D6",
                                outline="#8B5A2B", width=4, tags="dialogo")
        lienzo.create_text(cx, cy - 50, text=datos["pregunta"], font=("Comic Sans MS", 16, "bold"),
                           fill="#4A2C12", justify="center", tags="dialogo")
        zona_si = (cx - 220, cy + 50, cx - 20, cy + 110)
        zona_no = (cx + 20, cy + 50, cx + 220, cy + 110)
        lienzo.create_rectangle(zona_si, fill="#C0392B", outline="white", width=3, tags="dialogo")
        lienzo.create_rectangle(zona_no, fill="#C0392B", outline="white", width=3, tags="dialogo")
        lienzo.create_text((zona_si[0] + zona_si[2]) / 2, (zona_si[1] + zona_si[3]) / 2, text="SÍ",
                           fill="white", font=("Comic Sans MS", 18, "bold"), tags="dialogo")
        lienzo.create_text((zona_no[0] + zona_no[2]) / 2, (zona_no[1] + zona_no[3]) / 2, text="NO",
                           fill="white", font=("Comic Sans MS", 18, "bold"), tags="dialogo")
    actual = {"lienzo": lienzo, "si": zona_si, "no": zona_no, "al_si": al_si, "al_no": al_no}


def hay_dialogo():
    return actual is not None


def _dentro(zona, x, y):
    return zona[0] <= x <= zona[2] and zona[1] <= y <= zona[3]


def sobre_boton(x, y):
    """True si el mouse está sobre SÍ o NO."""
    if actual is None:
        return False
    return _dentro(actual["si"], x, y) or _dentro(actual["no"], x, y)


def cerrar():
    global actual
    if actual is not None:
        actual["lienzo"].delete("dialogo")
    actual = None


def clic(x, y):
    """Procesa un clic mientras hay un cuadro abierto. Ignora clics fuera de SÍ / NO."""
    if actual is None:
        return
    if _dentro(actual["si"], x, y):
        accion = actual["al_si"]
        cerrar()
        accion()
    elif _dentro(actual["no"], x, y):
        accion = actual["al_no"]
        cerrar()
        if accion is not None:
            accion()
