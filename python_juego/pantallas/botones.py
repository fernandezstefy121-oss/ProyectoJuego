# pantallas/botones.py
# Botones personalizados (redondeados, con sombra y color al pasar el mouse).
# Se dibujan sobre un Canvas, así que sirven para todas las pantallas del juego.


def rect_redondeado(lienzo, x1, y1, x2, y2, radio, **opciones):
    """Dibuja un rectángulo con esquinas redondeadas.
    Truco: un polígono con 'smooth=True' suaviza las esquinas."""
    puntos = [x1 + radio, y1,
              x2 - radio, y1,
              x2, y1,
              x2, y1 + radio,
              x2, y2 - radio,
              x2, y2,
              x2 - radio, y2,
              x1 + radio, y2,
              x1, y2,
              x1, y2 - radio,
              x1, y1 + radio,
              x1, y1]
    return lienzo.create_polygon(puntos, smooth=True, **opciones)


def crear_boton(lienzo, x, y, ancho, alto, texto, comando,
                color="#E74C3C", color_hover="#FF7B6B", tam_letra=22):
    """Crea un botón centrado en (x, y).
    'comando' es la función que se ejecuta al hacer clic.
    Devuelve el id del texto, por si luego hay que cambiarlo (por ejemplo, el botón de sonido)."""
    etiqueta = "boton_" + texto          # nombre interno para agrupar las 3 figuras del botón
    x1 = x - ancho // 2
    y1 = y - alto // 2
    x2 = x + ancho // 2
    y2 = y + alto // 2

    # 1) Sombra (da el efecto 3D)
    rect_redondeado(lienzo, x1 + 4, y1 + 7, x2 + 4, y2 + 7, 24,
                    fill="#0B2A4A", outline="", stipple="gray50", tags=etiqueta)
    # 2) Cuerpo del botón
    cuerpo = rect_redondeado(lienzo, x1, y1, x2, y2, 24,
                             fill=color, outline="white", width=4, tags=etiqueta)
    # 3) Texto
    id_texto = lienzo.create_text(x, y, text=texto, fill="white",
                                  font=("Comic Sans MS", tam_letra, "bold"), tags=etiqueta)

    # Eventos del mouse sobre cualquiera de las 3 figuras
    def al_entrar(evento):
        lienzo.itemconfig(cuerpo, fill=color_hover)
        lienzo.config(cursor="hand2")

    def al_salir(evento):
        lienzo.itemconfig(cuerpo, fill=color)
        lienzo.config(cursor="")

    def al_clic(evento):
        comando()

    lienzo.tag_bind(etiqueta, "<Enter>", al_entrar)
    lienzo.tag_bind(etiqueta, "<Leave>", al_salir)
    lienzo.tag_bind(etiqueta, "<Button-1>", al_clic)
    return id_texto
