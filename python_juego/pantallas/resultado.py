# pantallas/resultado.py
# Pantalla final: Victoria (gana Snoopy), Derrota (gana el Barón Rojo) o Empate.
# Los botones MENÚ PRINCIPAL y CONTINUAR ya vienen dentro de la imagen; aquí se ponen
# zonas de clic encima. El vídeo de nubes se ve detrás de la imagen.
import tkinter as tk
import tkinter.font as tkfont

from pantallas import animaciones, estado, sonidos, video
from pantallas.recursos import cargar_imagen

# Zonas medidas sobre cada imagen original: (x1, y1, x2, y2).
# 'texto' es el centro del pergamino donde se escribe el nombre.
PANTALLAS = {
    "X": {"archivo": "pantalla_victoria.png", "tam": (1298, 725),
          "menu": (672, 605, 965, 683), "continuar": (985, 605, 1268, 683),
          "texto": (955, 503), "ancho_texto": 330, "color": "#4A2C12"},
    "O": {"archivo": "pantalla_derrota.png", "tam": (1298, 725),
          "menu": (668, 607, 962, 683), "continuar": (982, 607, 1266, 683),
          "texto": (955, 505), "ancho_texto": 330, "color": "#4A2C12"},
    "EMPATE": {"archivo": "pantalla_empate.png", "tam": (1024, 572),
               "menu": (205, 462, 532, 545), "continuar": (552, 462, 866, 545),
               "texto": (500, 428), "ancho_texto": 360, "color": "#4A2C12"},
}


def crear_pantalla(ventana, ir_a, ancho, alto):
    marco = tk.Frame(ventana)
    lienzo = tk.Canvas(marco, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack()

    fondo = video.crear_fondo(lienzo, ventana, ancho, alto)
    zonas = {"menu": None, "continuar": None}
    activa = {"valor": False}           # True mientras esta pantalla está a la vista (para el confeti)

    def en_zona(zona, x, y):
        return zona is not None and zona[0] <= x <= zona[2] and zona[1] <= y <= zona[3]

    def al_mover(evento):
        sobre = en_zona(zonas["menu"], evento.x, evento.y) or en_zona(zonas["continuar"], evento.x, evento.y)
        lienzo.config(cursor="hand2" if sobre else "")

    def al_clic(evento):
        if en_zona(zonas["menu"], evento.x, evento.y):
            ir_a("inicio")
        elif en_zona(zonas["continuar"], evento.x, evento.y):
            ir_a("partida")             # misma pareja de jugadores, tablero nuevo

    lienzo.bind("<Motion>", al_mover)
    lienzo.bind("<Button-1>", al_clic)

    def dibujar_resultado():
        lienzo.delete("resultado", "confeti")
        datos = PANTALLAS.get(estado.resultado, PANTALLAS["EMPATE"])
        foto = cargar_imagen(datos["archivo"], ancho, alto)
        if foto is None:
            # Respaldo si falta la imagen
            lienzo.create_rectangle(250, 150, 850, 500, fill="#FFF4D6", outline="#8B5A2B",
                                    width=4, tags="resultado")
            lienzo.create_text(550, 250, text="Falta " + datos["archivo"], fill="#8B5A2B",
                               font=("Comic Sans MS", 20, "bold"), tags="resultado")
            zonas["menu"] = (300, 400, 520, 470)
            zonas["continuar"] = (580, 400, 800, 470)
            lienzo.create_text(410, 435, text="MENÚ PRINCIPAL", tags="resultado")
            lienzo.create_text(690, 435, text="CONTINUAR", tags="resultado")
            return
        lienzo.create_image(ancho / 2, alto / 2, image=foto, tags="resultado")
        esc = foto.width() / datos["tam"][0]
        izq = ancho / 2 - foto.width() / 2
        arr = alto / 2 - foto.height() / 2
        for nombre_zona in ("menu", "continuar"):
            z = datos[nombre_zona]
            zonas[nombre_zona] = (izq + z[0] * esc, arr + z[1] * esc, izq + z[2] * esc, arr + z[3] * esc)

        # Texto sobre el pergamino
        if estado.resultado == "X":
            texto = "¡Ganó " + estado.nombre_x + "!"
        elif estado.resultado == "O":
            texto = "¡Ganó " + estado.nombre_o + "!"
        else:
            return                      # en el empate no se escribe ningún texto
        maximo = datos["ancho_texto"] * esc
        tam = 30
        letra = tkfont.Font(family="Georgia", size=tam, weight="bold")
        while tam > 10 and letra.measure(texto) > maximo:
            tam = tam - 1
            letra.configure(size=tam)
        tx = izq + datos["texto"][0] * esc
        ty = arr + datos["texto"][1] * esc
        lienzo.create_text(tx, ty, text=texto, fill=datos["color"],
                           font=("Georgia", tam, "bold"), tags="resultado")

    def al_mostrar():
        activa["valor"] = True
        dibujar_resultado()
        video.iniciar(fondo)
        sonidos.efecto({"X": "victoria", "O": "derrota"}.get(estado.resultado, "empate"))
        if estado.resultado in ("X", "O"):
            piezas = animaciones.crear_confeti(lienzo, ancho, 90)
            animaciones.animar_confeti(ventana, lienzo, piezas, ancho, alto, lambda: activa["valor"])

    def al_ocultar():
        activa["valor"] = False
        video.detener(fondo)
        lienzo.delete("confeti")

    marco.al_mostrar = al_mostrar
    marco.al_ocultar = al_ocultar
    return marco
