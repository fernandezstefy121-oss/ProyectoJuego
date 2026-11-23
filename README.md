# Tres en Raya — Proyecto Integrador

**Carrera:** Ingeniería en Inteligencia Artificial · **Asignatura:** Fundamentos de Algoritmos
**Universidad:** UIDE · Quito, Ecuador · 2026

**Integrantes:** Ingrid Fernández · Francis Chamorro

Juego de **Tres en Raya** para dos jugadores con interfaz gráfica, historial de partidas y un
**ranking de jugadores**. El proyecto combina dos módulos que se comunican mediante un archivo CSV:

| Módulo | Lenguaje | Qué hace |
|---|---|---|
| `python_juego/` | Python | Lógica del juego, interfaz gráfica y registro de cada partida en `historial.csv` |
| `cpp_datos/` | C++ | Lee `historial.csv`, arma una lista enlazada, acumula los puntos de cada jugador y genera el ranking con Bubble Sort |

```
Python (juego)  ──escribe──▶  historial.csv  ◀──lee──  C++ (ranking)
```

## Estructura del proyecto

```
ProyectoJuego/
├── python_juego/
│   ├── juego.py          # punto de entrada del juego
│   ├── interfaz.py       # ventanas y eventos (Tkinter)
│   ├── logica.py         # reglas del juego
│   ├── historial.csv     # registro de partidas (lo comparten Python y C++)
│   ├── pantallas/        # pantallas del juego
│   │   ├── estado.py
│   │   ├── botones.py
│   │   ├── recursos.py
│   │   ├── inicio.py
│   │   ├── presentacion.py
│   │   ├── partida.py
│   │   ├── resultado.py
│   │   └── sonidos.py
│   └── assets/           # imágenes, video y sonidos (assets/sonidos/*.ogg)
├── cpp_datos/
│   ├── main.cpp          # programa principal del ranking
│   ├── ranking.cpp       # lectura del historial, puntos y Bubble Sort
│   └── nodo.h            # estructuras Nodo y JugadorRanking
├── LICENSE
└── README.md
```

## Cómo ejecutarlo

### 1. El juego (Python)

Requisitos: Python 3.8 o superior. Tkinter viene incluido con Python. Para el **sonido** se usa la librería `pygame` (`pip install pygame`). Es opcional: si no está instalada o no hay tarjeta de sonido, el juego funciona igual, sin sonido.

```bash
cd python_juego
python juego.py        # en algunos sistemas: python3 juego.py
```

Al terminar cada partida (victoria o empate) se agrega una fila a `historial.csv`.

### 2. El ranking (C++)

Hay que compilar **juntos** `main.cpp` y `ranking.cpp` (`nodo.h` es un encabezado y no se compila por separado).

```bash
cd cpp_datos
g++ -std=c++11 main.cpp ranking.cpp -o ranking
./ranking              # en Windows: ranking.exe
```

También se puede compilar con CMake: `cmake -B build && cmake --build build`.

El programa busca `historial.csv` en `python_juego/` y también acepta una ruta propia:
`./ranking ruta/al/historial.csv`.

## Cómo se comunican los dos módulos

Python y C++ comparten el archivo `historial.csv`, con cinco columnas:

```
id_partida,jugador_x,jugador_o,resultado,fecha
1,Ana,Beto,X,2026-11-17
2,Ana,Beto,EMPATE,2026-11-17
```

La columna `resultado` solo puede ser `X` (ganó el jugador X), `O` (ganó el jugador O) o `EMPATE`.

**Puntuación del ranking:** victoria = 3 puntos · empate = 1 punto · derrota = 0 puntos.

## Estructuras de datos y algoritmos

| Elemento | Dónde | Detalle |
|---|---|---|
| Matriz 3×3 | `logica.py` | Lista de listas: `tablero[fila][columna]`, con índices de 0 a 2 |
| Verificación de victoria | `logica.py` | Recorridos explícitos sobre los índices [0..2]: 3 filas, 3 columnas y las 2 diagonales (`i == j` e `i + j == 2`) |
| Pila (deshacer) | `logica.py` | `append` al hacer una jugada y `pop` al deshacerla (último en entrar, primero en salir) |
| Lista enlazada de partidas | `ranking.cpp` (`struct Nodo`) | Un nodo por cada fila de `historial.csv` |
| Lista de jugadores únicos | `ranking.cpp` (`struct JugadorRanking`) | Se recorre la lista de partidas y se acumulan los puntos de cada jugador **antes** de ordenar |
| Bubble Sort | `ranking.cpp` (`ordenarRanking`) | Ordena `JugadorRanking` de mayor a menor puntaje |

## Gestión del equipo

El punto crítico del desarrollo y su resolución con la Fórmula Asertiva (Hechos, Sentimientos,
Necesidades y Petición) están documentados en
[`Bitacora_de_Gestion_de_Conflictos.docx`](Bitacora_de_Gestion_de_Conflictos.docx).

## Declaración de Autoría

Los integrantes del equipo declaramos que este proyecto fue desarrollado para la asignatura
*Fundamentos de Algoritmos* y que:

1. El diseño, la lógica del juego, el módulo de ranking y la integración entre ambos módulos son trabajo del equipo.
2. Usamos herramientas de inteligencia artificial como apoyo. Cuáles y para qué se detalla en la sección
   **Créditos y recursos de terceros**.
3. No se copió código de terceros: de algunos tutoriales solo se tomaron ideas.
4. Todos los recursos visuales y de audio de terceros están citados a continuación.

| Integrante | Aportes principales |
|---|---|
| Ingrid Fernández | Lógica del juego en Python e interfaz gráfica (Tkinter) |
| Francis Chamorro | Módulo de C++ (lectura del historial, lista enlazada, puntos y ranking con Bubble Sort) y Bitácora de Gestión de Conflictos |

## Créditos y recursos de terceros

### Herramientas de inteligencia artificial

| Herramienta | Para qué se usó |
|---|---|
| Claude (Anthropic) | Ayuda para estructurar, escribir, probar y explicar el código de la lógica del juego en Python y del módulo de ranking en C++ (lista enlazada, JugadorRanking y Bubble Sort), para separar el módulo de C++ en `nodo.h`, `ranking.cpp` y `main.cpp`, y para redactar la documentación, incluida la Bitácora de Gestión de Conflictos a partir de los hechos que el equipo contó. El equipo revisó, probó y adaptó el código y los textos. |
| ChatGPT (OpenAI) | Generar los diseños de la interfaz gráfica |
| Gemini (Google) | Quitar el fondo de imágenes y diseñar el panel de victorias y empate |

### Código de terceros y librerías

- Python, biblioteca estándar: `tkinter` (incluido `messagebox`), `datetime` y `os`.
- Python, librería externa: `pygame` (solo `pygame.mixer`, para música y efectos de sonido; licencia LGPL). Es opcional para jugar.
- C++: biblioteca estándar (STL).
- No se utilizó código de terceros: solo se vieron ideas en tutoriales, sin copiar código.

### Recursos visuales

- Imágenes de Pinterest (temática Snoopy):
  - https://pin.it/6rrUfrXyZ
  - https://pin.it/4naG5W4vo
  - https://pin.it/2HjxZEs3a
  - https://pin.it/Qvb2OTx3Z
  - https://pin.it/3QjrQXSe4
  - https://pin.it/4a0WbEtcp
  - https://pin.it/46CQEuCbv
- Los personajes de Snoopy/Peanuts pertenecen a sus titulares y se usan solo con fines educativos, sin fines de lucro.

### Video

- Time-lapse de nubes: Pexels — https://www.pexels.com/es-es/video/impresionante-time-lapse-de-nubes-cumulos-esponjosas-32985050/

### Efectos de sonido (Pixabay)

| Uso | Efecto | Enlace |
|---|---|---|
| Colocar ficha | clean minimal pop | https://pixabay.com/es/sound-effects/clean-minimal-pop-467466/ |
| Casilla ocupada | error notification 08 | https://pixabay.com/es/sound-effects/pel%C3%ADculas-y-efectos-especiales-error-notification-08-206492/ |
| Victoria | cute happy victory | https://pixabay.com/es/sound-effects/cute-happy-victory-476376/ |
| Derrota | losing horn | https://pixabay.com/es/sound-effects/pel%C3%ADculas-y-efectos-especiales-losing-horn-313723/ |
| Empate | lose sfx | https://pixabay.com/es/sound-effects/pel%C3%ADculas-y-efectos-especiales-lose-sfx-365579/ |

### Canciones

- "M.E." — Gary Numan.
- "where's my head at _" — 100 gecs & Basement Jaxx.

Las canciones pertenecen a sus artistas y sellos, y se usan solo con fines educativos, sin fines de lucro.

## Licencia

Este proyecto se distribuye bajo la **Licencia MIT** (código abierto). Consulta el archivo [`LICENSE`](LICENSE).
La licencia cubre el **código escrito por el equipo**; las imágenes, canciones, efectos de sonido y videos
de terceros conservan los derechos de sus respectivos autores, como se indica en los créditos.
