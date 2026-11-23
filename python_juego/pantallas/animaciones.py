# pantallas/animaciones.py
# Animaciones con after(): la ventana nunca se congela porque en vez de esperar,
# cada "paso" se programa para ejecutarse unos milisegundos después.
import random

COLORES_CONFETI = ["#F1C40F", "#E74C3C", "#3498DB", "#2ECC71", "#9B59B6", "#FFFFFF", "#F39C12"]


def punto_curva(inicio, control, fin, t):
    """Punto de una curva (Bézier) entre 'inicio' y 'fin', con 'control' que la dobla.
    t va de 0 (inicio) a 1 (fin)."""
    x = (1 - t) ** 2 * inicio[0] + 2 * (1 - t) * t * control[0] + t ** 2 * fin[0]
    y = (1 - t) ** 2 * inicio[1] + 2 * (1 - t) * t * control[1] + t ** 2 * fin[1]
    return (x, y)


def volar_en_curva(ventana, lienzo, etiqueta, inicio, control, fin, pasos, ms, al_terminar):
    """Mueve todo lo que tenga la 'etiqueta' siguiendo una curva de 'inicio' a 'fin'."""
    estado = {"paso": 0, "x": inicio[0], "y": inicio[1]}

    def dar_paso():
        estado["paso"] = estado["paso"] + 1
        t = estado["paso"] / pasos
        punto = punto_curva(inicio, control, fin, t)
        lienzo.move(etiqueta, punto[0] - estado["x"], punto[1] - estado["y"])
        estado["x"] = punto[0]
        estado["y"] = punto[1]
        if estado["paso"] < pasos:
            ventana.after(ms, dar_paso)
        else:
            al_terminar()

    ventana.after(ms, dar_paso)


def deslizar(ventana, lienzo, etiqueta, dx, dy, pasos=24, ms=16, al_terminar=None):
    """Desliza lo que tenga la 'etiqueta' (dx, dy) píxeles, empezando rápido y frenando suave."""
    estado = {"paso": 0, "anterior": 0.0}

    def dar_paso():
        estado["paso"] = estado["paso"] + 1
        t = estado["paso"] / pasos
        avance = 1 - (1 - t) ** 3
        lienzo.move(etiqueta, dx * (avance - estado["anterior"]), dy * (avance - estado["anterior"]))
        estado["anterior"] = avance
        if estado["paso"] < pasos:
            ventana.after(ms, dar_paso)
        elif al_terminar is not None:
            al_terminar()

    ventana.after(ms, dar_paso)


def crear_confeti(lienzo, ancho, cantidad=90, colores=COLORES_CONFETI):
    """Crea papelitos de colores arriba de la pantalla. Devuelve la lista de papelitos."""
    piezas = []
    for i in range(cantidad):
        x = random.randint(0, ancho)
        y = random.randint(-650, 0)
        w = random.randint(6, 12)
        h = random.randint(8, 16)
        item = lienzo.create_rectangle(x, y, x + w, y + h, fill=random.choice(colores),
                                       outline="", tags="confeti")
        piezas.append({"item": item, "x": x, "y": y, "w": w, "h": h,
                       "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(3, 7)})
    return piezas


def animar_confeti(ventana, lienzo, piezas, ancho, alto, esta_activo):
    """Hace caer el confeti. Se detiene solo cuando esta_activo() devuelve False."""
    def paso():
        if not esta_activo():
            return
        for p in piezas:
            p["x"] = p["x"] + p["vx"]
            p["y"] = p["y"] + p["vy"]
            if p["y"] > alto:                # al salir por abajo, vuelve a caer desde arriba
                p["y"] = -20
                p["x"] = random.randint(0, ancho)
            lienzo.coords(p["item"], p["x"], p["y"], p["x"] + p["w"], p["y"] + p["h"])
        ventana.after(30, paso)

    ventana.after(30, paso)
