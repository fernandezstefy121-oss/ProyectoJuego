#ifndef NODO_H
#define NODO_H

#include <string>

// Una partida del historial (un nodo de la lista enlazada de partidas)
struct Nodo {
    int id_partida;
    std::string jugador_x;
    std::string jugador_o;
    std::string resultado;      // "X", "O" o "EMPATE"
    std::string fecha;
    Nodo* siguiente;
};

// Un jugador único con sus puntos acumulados (lista enlazada del ranking)
struct JugadorRanking {
    std::string nombre;
    int puntos;
    JugadorRanking* siguiente;
};

// Funciones (están escritas en ranking.cpp)
Nodo* leerHistorial(const std::string& ruta);               // 1. lee el CSV y arma la lista de partidas
JugadorRanking* calcularPuntos(Nodo* primera_partida);      // 2. acumula los puntos por jugador
void ordenarRanking(JugadorRanking* primer_jugador);        // 3. Bubble Sort de mayor a menor
void mostrarRanking(JugadorRanking* primer_jugador);        // 4. muestra el ranking
void liberarPartidas(Nodo* primera_partida);                // 5. libera la memoria de las listas
void liberarRanking(JugadorRanking* primer_jugador);

#endif
