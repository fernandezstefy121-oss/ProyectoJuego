# pantallas/sonidos.py
# Música y efectos con pygame.mixer. Un solo interruptor (sonido_activo) controla todo.
# Si pygame no está instalado o no hay tarjeta de sonido, el juego funciona igual, sin sonido.
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(BASE, "assets", "sonidos")

MUSICAS = {"menu": "musica_menu.ogg", "partida": "musica_partida.ogg"}
EFECTOS = {"ficha": "ficha.ogg", "ocupada": "ocupada.ogg", "victoria": "victoria.ogg",
           "derrota": "derrota.ogg", "empate": "empate.ogg"}

sonido_activo = True
musica_actual = None        # qué música "toca" ahora (aunque el sonido esté apagado)
_pygame = None              # el módulo pygame, o None si no se pudo usar
_efectos = {}               # efectos ya cargados


def iniciar():
    """Prepara el mezclador de audio. Se llama una vez al abrir el programa."""
    global _pygame
    try:
        import pygame
        pygame.mixer.init()
        _pygame = pygame
        for nombre, archivo in EFECTOS.items():
            ruta = os.path.join(CARPETA, archivo)
            if os.path.exists(ruta):
                sonido = pygame.mixer.Sound(ruta)
                sonido.set_volume(0.9)
                _efectos[nombre] = sonido
    except Exception:
        _pygame = None


def _tocar_musica():
    if _pygame is None or musica_actual is None:
        return
    ruta = os.path.join(CARPETA, MUSICAS[musica_actual])
    if not os.path.exists(ruta):
        return
    try:
        _pygame.mixer.music.load(ruta)
        _pygame.mixer.music.set_volume(0.5)
        _pygame.mixer.music.play(-1)          # -1 = repetir sin parar
    except Exception:
        pass


def musica(nombre):
    """Cambia la música: "menu", "partida" o None (silencio). Si ya suena esa, no la reinicia."""
    global musica_actual
    if nombre == musica_actual:
        return
    musica_actual = nombre
    if _pygame is not None:
        try:
            _pygame.mixer.music.stop()
        except Exception:
            pass
    if sonido_activo:
        _tocar_musica()


def efecto(nombre):
    """Reproduce un efecto corto ("ficha", "ocupada", "victoria", "derrota", "empate")."""
    if sonido_activo and nombre in _efectos:
        _efectos[nombre].play()


def alternar():
    """Activa o desactiva TODO el sonido. Devuelve el estado nuevo."""
    global sonido_activo
    sonido_activo = not sonido_activo
    if _pygame is not None:
        try:
            if sonido_activo:
                _tocar_musica()
            else:
                _pygame.mixer.music.stop()
                _pygame.mixer.stop()
        except Exception:
            pass
    return sonido_activo
