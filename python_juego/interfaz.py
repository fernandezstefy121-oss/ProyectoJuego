# interfaz.py - Ventana principal y cambio de pantallas (se ejecuta con: python interfaz.py)
# Crea la ventana UNA sola vez y cambia entre pantallas (frames).
import tkinter as tk
from tkinter import messagebox

from pantallas import inicio, presentacion, partida, resultado, sonidos

ANCHO = 1100
ALTO = 650

ventana = tk.Tk()
ventana.title("Snoopy vs. Barón Rojo")
ventana.resizable(False, False)

# Centrar la ventana en la pantalla
x = (ventana.winfo_screenwidth() - ANCHO) // 2
y = (ventana.winfo_screenheight() - ALTO) // 2
ventana.geometry(str(ANCHO) + "x" + str(ALTO) + "+" + str(x) + "+" + str(y))

pantallas = {}                 # nombre de la pantalla -> su Frame
# Qué música suena en cada pantalla (None = silencio; en el resultado suena un efecto corto)
MUSICA = {"inicio": "menu", "presentacion": "menu", "partida": "partida", "resultado": None}
sonidos.iniciar()
pantalla_actual = None


def ir_a(nombre):
    """Esconde la pantalla actual y muestra la que se pidió."""
    global pantalla_actual
    if nombre not in pantallas:
        messagebox.showinfo("En construcción", "La pantalla '" + nombre + "' aún no está lista.")
        return
    if pantalla_actual is not None:
        # Si la pantalla tiene algo que detener al salir (por ejemplo, el vídeo), se ejecuta
        al_salir = getattr(pantalla_actual, "al_ocultar", None)
        if al_salir is not None:
            al_salir()
        pantalla_actual.pack_forget()
    pantalla_actual = pantallas[nombre]
    pantalla_actual.pack()
    sonidos.musica(MUSICA.get(nombre))
    # Si la pantalla tiene algo que preparar al mostrarse, se ejecuta
    preparar = getattr(pantalla_actual, "al_mostrar", None)
    if preparar is not None:
        preparar()


pantallas["inicio"] = inicio.crear_pantalla(ventana, ir_a, ANCHO, ALTO)
pantallas["presentacion"] = presentacion.crear_pantalla(ventana, ir_a, ANCHO, ALTO)
pantallas["partida"] = partida.crear_pantalla(ventana, ir_a, ANCHO, ALTO)
pantallas["resultado"] = resultado.crear_pantalla(ventana, ir_a, ANCHO, ALTO)

ir_a("inicio")
ventana.mainloop()