#include <iostream>
#include <fstream>
#include <string>
#include "nodo.h"
using namespace std;

int main(int argc, char* argv[]) {
    // Rutas donde puede estar el historial según desde dónde se ejecute el programa.
    // También se puede indicar una ruta al ejecutar:  ./ranking ruta/historial.csv
    string rutas[] = {
        "../../python_juego/historial.csv",
        "../python_juego/historial.csv",
        "python_juego/historial.csv",
        "historial.csv"
    };

    string ruta = rutas[0];
    if (argc > 1) {
        ruta = argv[1];
    } else {
        for (int i = 0; i < 4; i++) {                   // usa la primera ruta que exista
            ifstream prueba(rutas[i]);
            if (prueba.is_open()) {
                ruta = rutas[i];
                break;
            }
        }
    }

    Nodo* primera_partida = leerHistorial(ruta);                    // 1. leer el historial
    if (primera_partida == nullptr) {
        cout << "No hay partidas para mostrar." << endl;
        return 0;
    }

    JugadorRanking* primer_jugador = calcularPuntos(primera_partida);   // 2. calcular puntos
    ordenarRanking(primer_jugador);                                     // 3. ordenar (Bubble Sort)
    mostrarRanking(primer_jugador);                                     // 4. mostrar

    liberarPartidas(primera_partida);                                   // 5. liberar memoria
    liberarRanking(primer_jugador);

    return 0;
}
