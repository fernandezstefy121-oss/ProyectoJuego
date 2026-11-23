# pantallas/partida.py
# Pantalla de la partida: video de nubes de fondo, tablero, marcador, avión de turno,
# avionetas que dejan las fichas y botones. Las reglas NO están aquí: se usan las de juego.py.
import tkinter as tk
import tkinter.font as tkfont

import juego
from pantallas import animaciones, dialogos, estado, marcador, sonidos, video
from pantallas.inicio import texto_con_borde
from pantallas.recursos import cargar_imagen, dibujar_imagen

# ---------- Medidas del tablero ----------
X0 = 311            # esquina izquierda del tablero
Y0 = 160            # esquina de arriba del tablero
ANCHO_CASILLA = 150
ALTO_CASILLA = 119
SEPARACION = 14

# ---------- Panel del marcador (medidas de la imagen original 1213x785) ----------
ANCHO_PANEL = 280
ESCALA_PANEL = ANCHO_PANEL / 1213
CAJA_VICTORIAS = (887, 225)       # centro de la caja de arriba, dentro de la imagen
CAJA_EMPATES = (887, 560)         # centro de la caja de abajo

# ---------- Banner de turno (tamaño de la imagen y dónde va el texto dentro de ella) ----------
BANNERS = {
    "X": {"archivo": "turno_snoopy.png", "tam": (422, 129), "texto": (148, 90), "ancho_texto": 272},
    "O": {"archivo": "turno_baron.png", "tam": (540, 125), "texto": (404, 74), "ancho_texto": 269},
}
Y_BANNER = 92

# ---------- Botones de abajo ----------
BOTONES_Y = 592


def crear_pantalla(ventana, ir_a, ancho, alto):
    marco = tk.Frame(ventana)
    lienzo = tk.Canvas(marco, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack()

    fondo = video.crear_fondo(lienzo, ventana, ancho, alto)

    fichas = {}              # (fila, columna) -> id de la imagen de la ficha
    botones = []             # lista de (x1, y1, x2, y2, acción)
    bloqueado = {"valor": False}     # True mientras hay animaciones: no se aceptan clics
    pantalla = {"id": 0}     # sube cada vez que se abre la pantalla; sirve para ignorar callbacks viejos

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------
    def zona_casilla(fila, columna):
        x1 = X0 + columna * (ANCHO_CASILLA + SEPARACION)
        y1 = Y0 + fila * (ALTO_CASILLA + SEPARACION)
        return (x1, y1, x1 + ANCHO_CASILLA, y1 + ALTO_CASILLA)

    def centro_casilla(fila, columna):
        z = zona_casilla(fila, columna)
        return ((z[0] + z[2]) / 2, (z[1] + z[3]) / 2)

    def dibujar_tablero():
        for fila in range(3):
            for columna in range(3):
                z = zona_casilla(fila, columna)
                cx, cy = centro_casilla(fila, columna)
                foto = cargar_imagen("casilla_nube.png", ANCHO_CASILLA, ALTO_CASILLA)
                if foto is not None:
                    lienzo.create_image(cx, cy, image=foto, tags="tablero")
                else:
                    lienzo.create_rectangle(z[0], z[1], z[2], z[3], fill="#EAF6FF",
                                            outline="white", width=3, tags="tablero")

    def dibujar_ficha(fila, columna, turno):
        cx, cy = centro_casilla(fila, columna)
        archivo = "snoopy_ficha.png" if turno == "X" else "baron_ficha.png"
        id_ficha = dibujar_imagen(lienzo, archivo, cx, cy, 120, 95, tags="ficha")
        fichas[(fila, columna)] = id_ficha

    def dibujar_lateral(lado):
        """Dibuja a un personaje: su imagen (apagada si no es su turno), su nombre y su marcador."""
        turno = "X" if lado == "snoopy" else "O"
        cx = 155 if lado == "snoopy" else ancho - 155
        activo = (juego.turno_actual() == turno)
        archivo = "snoopy_ficha.png" if lado == "snoopy" else "baron_ficha.png"
        nombre = estado.nombre_x if lado == "snoopy" else estado.nombre_o

        dibujar_imagen(lienzo, archivo, cx, 135, 230, 150, opacidad=1.0 if activo else 0.45, tags="ui")
        texto_con_borde(lienzo, cx, 240, nombre, 22, tags="ui")

        # Panel del marcador
        py = 405
        dibujar_imagen(lienzo, "panel_marcador.png", cx, py, ANCHO_PANEL, None, tags="ui")
        foto = cargar_imagen("panel_marcador.png", ANCHO_PANEL)
        if foto is not None:
            izq = cx - foto.width() / 2
            arr = py - foto.height() / 2
            esc = foto.width() / 1213
        else:
            izq = cx - ANCHO_PANEL / 2
            arr = py - 90
            esc = ESCALA_PANEL
        victorias = marcador.datos["snoopy"] if lado == "snoopy" else marcador.datos["baron"]
        lienzo.create_text(izq + CAJA_VICTORIAS[0] * esc, arr + CAJA_VICTORIAS[1] * esc,
                           text=str(victorias), fill="#F5E6C8", font=("Georgia", 40, "bold"), tags="ui")
        lienzo.create_text(izq + CAJA_EMPATES[0] * esc, arr + CAJA_EMPATES[1] * esc,
                           text=str(marcador.datos["empates"]), fill="#F5E6C8",
                           font=("Georgia", 40, "bold"), tags="ui")

    def dibujar_boton(archivo, x, accion, tag=""):
        """Dibuja un botón-imagen centrado en x y guarda su zona de clic."""
        y = BOTONES_Y
        foto = cargar_imagen(archivo, 200, 72)
        if foto is not None:
            lienzo.create_image(x, y, image=foto, tags=("ui", tag) if tag else "ui")
            w = foto.width() / 2
            h = foto.height() / 2
        else:
            w, h = 100, 35
            lienzo.create_rectangle(x - w, y - h, x + w, y + h, fill="#C0392B", outline="white",
                                    width=3, tags=("ui", tag) if tag else "ui")
            lienzo.create_text(x, y, text=archivo.replace(".png", ""), fill="white",
                               font=("Comic Sans MS", 11, "bold"), tags=("ui", tag) if tag else "ui")
        botones.append((x - w, y - h, x + w, y + h, accion))

    def dibujar_botones():
        del botones[:]
        dibujar_boton("btn_nueva_partida.png", 170, pedir_reiniciar)
        dibujar_boton("btn_deshacer.png", 410, pedir_deshacer)
        dibujar_boton("btn_menu_principal.png", 690, pedir_menu)
        archivo = "btn_sonido_on.png" if sonidos.sonido_activo else "btn_sonido_off.png"
        dibujar_boton(archivo, 930, alternar_sonido, tag="btn_sonido")

    def refrescar_ui():
        """Redibuja los laterales y botones (por ejemplo después de cambiar el turno)."""
        lienzo.delete("ui")
        dibujar_lateral("snoopy")
        dibujar_lateral("baron")
        dibujar_botones()

    # ------------------------------------------------------------------
    # Banner de turno: avión que arrastra una pancarta "TURNO DE <nombre>"
    # ------------------------------------------------------------------
    def mostrar_banner(turno, animar=True):
        lienzo.delete("banner")
        datos = BANNERS[turno]
        nombre = estado.nombre_x if turno == "X" else estado.nombre_o
        texto = "TURNO DE " + nombre.upper()
        cx = ancho / 2
        foto = cargar_imagen(datos["archivo"])
        if foto is not None:
            lienzo.create_image(cx, Y_BANNER, image=foto, tags="banner")
            tx = cx + (datos["texto"][0] - datos["tam"][0] / 2)
            ty = Y_BANNER + (datos["texto"][1] - datos["tam"][1] / 2)
            maximo = datos["ancho_texto"]
        else:
            lienzo.create_rectangle(cx - 220, Y_BANNER - 40, cx + 220, Y_BANNER + 40,
                                    fill="#FFF4D6", outline="#8B5A2B", width=3, tags="banner")
            tx, ty, maximo = cx, Y_BANNER, 380
        # Se busca la letra más grande que quepa en la pancarta
        tam = 20
        letra = tkfont.Font(family="Comic Sans MS", size=tam, weight="bold")
        while tam > 9 and letra.measure(texto) > maximo:
            tam = tam - 1
            letra.configure(size=tam)
        color = "#7A2E12" if turno == "X" else "#6B1414"
        lienzo.create_text(tx, ty, text=texto, fill=color, font=("Comic Sans MS", tam, "bold"), tags="banner")
        if animar:
            # Snoopy entra volando desde la izquierda; el Barón, desde la derecha
            salto = -(cx + 330) if turno == "X" else (ancho - cx + 330)
            lienzo.move("banner", salto, 0)
            animaciones.deslizar(ventana, lienzo, "banner", -salto, 0, pasos=28, ms=16)

    def mostrar_aviso(texto):
        lienzo.delete("aviso")
        lienzo.create_text(ancho / 2 + 2, 575, text=texto, fill="#123A6B", tags="aviso",
                           font=("Comic Sans MS", 18, "bold"))
        lienzo.create_text(ancho / 2, 573, text=texto, fill="white", tags="aviso",
                           font=("Comic Sans MS", 18, "bold"))
        mi_id = pantalla["id"]
        ventana.after(1400, lambda: lienzo.delete("aviso") if pantalla["id"] == mi_id else None)

    # ------------------------------------------------------------------
    # Jugar: la avioneta vuela a la casilla, deja la ficha y se va
    # ------------------------------------------------------------------
    def jugar_en(fila, columna):
        turno = juego.turno_actual()
        resultado = juego.poner_ficha(fila, columna)
        if resultado != "ok":
            sonidos.efecto("ocupada")
            mostrar_aviso("¡Esa casilla ya está ocupada!")
            return
        bloqueado["valor"] = True
        mi_id = pantalla["id"]
        destino = centro_casilla(fila, columna)
        desde_izq = (turno == "X")             # Snoopy llega por la izquierda; el Barón, por la derecha
        inicio = (-100, 120) if desde_izq else (ancho + 100, 120)
        salida = (ancho + 130, 60) if desde_izq else (-130, 60)
        archivo = "avion_snoopy.png" if turno == "X" else "avion_baron.png"
        dibujar_imagen(lienzo, archivo, inicio[0], inicio[1], 110, 100, tags="avioneta")
        mitad_x = (inicio[0] + destino[0]) / 2
        control_1 = (mitad_x, destino[1] - 230)

        def al_llegar():
            if pantalla["id"] != mi_id:
                return
            dibujar_ficha(fila, columna, turno)          # la ficha aparece en la casilla
            sonidos.efecto("ficha")
            control_2 = ((destino[0] + salida[0]) / 2, destino[1] - 200)
            animaciones.volar_en_curva(ventana, lienzo, "avioneta", destino, control_2, salida,
                                       22, 16, al_despegar)

        def al_despegar():
            if pantalla["id"] != mi_id:
                return
            lienzo.delete("avioneta")
            revisar_resultado(turno)

        animaciones.volar_en_curva(ventana, lienzo, "avioneta", inicio, control_1, destino,
                                   26, 16, al_llegar)

    def revisar_resultado(turno):
        linea = juego.linea_ganadora(turno)
        if len(linea) > 0:
            terminar(turno, linea)
        elif juego.jugadas == 9:
            terminar("EMPATE", [])
        else:
            bloqueado["valor"] = False
            refrescar_ui()
            mostrar_banner(juego.turno_actual())

    def terminar(resultado, linea):
        """Guarda la partida en el CSV y en el marcador y pasa a la pantalla de resultado."""
        juego.guardar_partida(estado.nombre_x, estado.nombre_o, resultado)
        marcador.sumar_resultado(resultado)
        estado.resultado = resultado
        mi_id = pantalla["id"]

        def ir_al_resultado():
            if pantalla["id"] == mi_id:
                ir_a("resultado")

        if len(linea) == 0:
            ventana.after(900, ir_al_resultado)
            return
        # Se resalta la línea ganadora parpadeando
        marcos = []
        for (f, c) in linea:
            z = zona_casilla(f, c)
            marcos.append(lienzo.create_rectangle(z[0] - 4, z[1] - 4, z[2] + 4, z[3] + 4,
                                                  outline="#F1C40F", width=6, tags="linea"))
        pasos = {"n": 0}

        def parpadear():
            if pantalla["id"] != mi_id:
                return
            pasos["n"] = pasos["n"] + 1
            visible = (pasos["n"] % 2 == 1)
            for m in marcos:
                lienzo.itemconfig(m, state="normal" if visible else "hidden")
            if pasos["n"] < 8:
                ventana.after(220, parpadear)
            else:
                ventana.after(500, ir_al_resultado)

        parpadear()

    # ------------------------------------------------------------------
    # Botones (con confirmación SÍ / NO)
    # ------------------------------------------------------------------
    def pedir_reiniciar():
        dialogos.mostrar(lienzo, ancho, alto, "reiniciar", reiniciar)

    def pedir_deshacer():
        if len(juego.pila) == 0:
            mostrar_aviso("Todavía no hay jugadas para deshacer")
            return
        dialogos.mostrar(lienzo, ancho, alto, "deshacer", deshacer)

    def pedir_menu():
        dialogos.mostrar(lienzo, ancho, alto, "menu", lambda: ir_a("inicio"))

    def reiniciar():
        empezar()

    def deshacer():
        ultima = juego.deshacer()
        if ultima is None:
            return
        id_ficha = fichas.pop((ultima[0], ultima[1]), None)
        if id_ficha is not None:
            lienzo.delete(id_ficha)
        refrescar_ui()
        mostrar_banner(juego.turno_actual())

    def alternar_sonido():
        sonidos.alternar()
        refrescar_ui()

    # ------------------------------------------------------------------
    # Mouse
    # ------------------------------------------------------------------
    def en_zona(zona, x, y):
        return zona[0] <= x <= zona[2] and zona[1] <= y <= zona[3]

    def al_mover(evento):
        if dialogos.hay_dialogo():
            sobre = dialogos.sobre_boton(evento.x, evento.y)
        elif bloqueado["valor"]:
            sobre = False
        else:
            sobre = False
            for b in botones:
                if en_zona(b, evento.x, evento.y):
                    sobre = True
            for f in range(3):
                for c in range(3):
                    if en_zona(zona_casilla(f, c), evento.x, evento.y):
                        sobre = True
        lienzo.config(cursor="hand2" if sobre else "")

    def al_clic(evento):
        if dialogos.hay_dialogo():
            dialogos.clic(evento.x, evento.y)
            return
        if bloqueado["valor"]:
            return                                  # hay animación en curso: se ignoran los clics
        for b in botones:
            if en_zona(b, evento.x, evento.y):
                b[4]()
                return
        for f in range(3):
            for c in range(3):
                if en_zona(zona_casilla(f, c), evento.x, evento.y):
                    jugar_en(f, c)
                    return

    lienzo.bind("<Motion>", al_mover)
    lienzo.bind("<Button-1>", al_clic)

    # ------------------------------------------------------------------
    # Entrar / salir de la pantalla
    # ------------------------------------------------------------------
    def empezar():
        """Prepara una partida nueva con los mismos jugadores."""
        juego.nuevo_juego()
        fichas.clear()
        bloqueado["valor"] = False
        pantalla["id"] = pantalla["id"] + 1
        dialogos.cerrar()
        lienzo.delete("tablero", "ficha", "ui", "banner", "aviso", "linea", "avioneta", "dialogo")
        dibujar_tablero()
        refrescar_ui()
        mostrar_banner("X")

    def al_mostrar():
        marcador.cargar()
        empezar()
        video.iniciar(fondo)

    def al_ocultar():
        pantalla["id"] = pantalla["id"] + 1
        video.detener(fondo)
        dialogos.cerrar()

    marco.al_mostrar = al_mostrar
    marco.al_ocultar = al_ocultar
    return marco
