# pantallas/presentacion.py
# Pantalla donde cada jugador escribe su nombre (uno con Snoopy y otro con el Barón Rojo)
# y después se muestra la presentación de los dos durante unos segundos.
import tkinter as tk

from pantallas import estado
from pantallas.botones import crear_boton, rect_redondeado
from pantallas.inicio import texto_con_borde
from pantallas.recursos import dibujar_cielo, dibujar_imagen

SEGUNDOS_PRESENTACION = 3
MAX_LETRAS = 14


def crear_pantalla(ventana, ir_a, ancho, alto):
    marco = tk.Frame(ventana)
    lienzo = tk.Canvas(marco, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack()

    # Las casillas de texto se crean una sola vez y se vuelven a colocar cada vez
    entrada_x = tk.Entry(marco, font=("Comic Sans MS", 16), justify="center", width=16, bd=3)
    entrada_o = tk.Entry(marco, font=("Comic Sans MS", 16), justify="center", width=16, bd=3)

    def tarjeta(x1, y1, x2, y2):
        """Recuadro crema con sombra, para cada jugador."""
        rect_redondeado(lienzo, x1 + 6, y1 + 8, x2 + 6, y2 + 8, 30,
                        fill="#0B2A4A", outline="", stipple="gray50")
        rect_redondeado(lienzo, x1, y1, x2, y2, 30,
                        fill="#FFF4D6", outline="#8B5A2B", width=4)

    # ---------- Parte 1: escribir los nombres ----------
    def mostrar_formulario():
        lienzo.delete("all")
        dibujar_cielo(lienzo, ancho, alto)
        texto_con_borde(lienzo, ancho // 2, 60, "¿QUIÉNES VUELAN HOY?", 40)

        tarjeta(60, 115, 520, 525)
        tarjeta(580, 115, 1040, 525)

        dibujar_imagen(lienzo, "snoopy_ficha.png", 290, 265, 300, 230)
        lienzo.create_text(290, 400, text="SNOOPY", fill="#C0392B",
                           font=("Comic Sans MS", 26, "bold"))
        lienzo.create_text(290, 435, text="Jugador 1 · ficha X", fill="#5D4037",
                           font=("Comic Sans MS", 14))
        lienzo.create_window(290, 480, window=entrada_x)

        dibujar_imagen(lienzo, "baron_ficha.png", 810, 265, 380, 230)
        lienzo.create_text(810, 400, text="BARÓN ROJO", fill="#7B241C",
                           font=("Comic Sans MS", 26, "bold"))
        lienzo.create_text(810, 435, text="Jugador 2 · ficha O", fill="#5D4037",
                           font=("Comic Sans MS", 14))
        lienzo.create_window(810, 480, window=entrada_o)

        crear_boton(lienzo, ancho // 2, 612, 300, 56, "¡A VOLAR!", comenzar,
                    color="#F39C12", color_hover="#FFB547", tam_letra=24)
        crear_boton(lienzo, 120, 612, 170, 50, "VOLVER", volver,
                    color="#2E86C1", color_hover="#5DADE2", tam_letra=18)
        entrada_x.focus_set()

    def mensaje(texto):
        """Muestra un aviso en rojo debajo de las tarjetas."""
        lienzo.delete("mensaje")
        lienzo.create_text(ancho // 2, 555, text=texto, fill="#922B21", tags="mensaje",
                           font=("Comic Sans MS", 15, "bold"))

    def volver():
        ir_a("inicio")

    def comenzar():
        """Revisa los nombres. Si están bien, los guarda y muestra la presentación."""
        nombre_x = entrada_x.get().strip()
        nombre_o = entrada_o.get().strip()
        if nombre_x == "" or nombre_o == "":
            mensaje("Escriban el nombre de los dos jugadores")
            return
        if "," in nombre_x or "," in nombre_o:
            mensaje("Los nombres no pueden tener comas")      # la coma rompería el CSV
            return
        if len(nombre_x) > MAX_LETRAS or len(nombre_o) > MAX_LETRAS:
            mensaje("Máximo " + str(MAX_LETRAS) + " letras por nombre")
            return
        estado.nombre_x = nombre_x
        estado.nombre_o = nombre_o
        mostrar_presentacion()

    # ---------- Parte 2: presentación de los dos jugadores ----------
    def mostrar_presentacion():
        lienzo.delete("all")
        dibujar_cielo(lienzo, ancho, alto)
        texto_con_borde(lienzo, ancho // 2, 70, "¡COMIENZA EL COMBATE!", 44)

        dibujar_imagen(lienzo, "snoopy_ficha.png", 260, 310, 340, 330)
        texto_con_borde(lienzo, 260, 520, estado.nombre_x, 30)
        texto_con_borde(lienzo, 260, 575, "SNOOPY · Jugador 1 (X)", 15)

        texto_con_borde(lienzo, ancho // 2, 320, "VS.", 70, color="#F7DC6F")

        dibujar_imagen(lienzo, "baron_ficha.png", 840, 310, 400, 270)
        texto_con_borde(lienzo, 840, 520, estado.nombre_o, 30)
        texto_con_borde(lienzo, 840, 575, "BARÓN ROJO · Jugador 2 (O)", 15)

        # Después de unos segundos pasa solo a la partida (after = "espera sin congelar la ventana")
        ventana.after(SEGUNDOS_PRESENTACION * 1000, lambda: ir_a("partida"))

    entrada_x.bind("<Return>", lambda evento: entrada_o.focus_set())
    entrada_o.bind("<Return>", lambda evento: comenzar())

    # main.py llama a esta función cada vez que se muestra la pantalla
    marco.al_mostrar = mostrar_formulario
    return marco
