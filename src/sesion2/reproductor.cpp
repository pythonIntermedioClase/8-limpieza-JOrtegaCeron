// src/sesion2/reproductor.cpp
#include "reproductor.h"

#include <iostream>


void mostrar_cancion(const Cancion& cancion) {
    std::cout << cancion.titulo << " - " << cancion.artista
               << " (" << cancion.genero << ", "
               << cancion.reproducciones << " reproducciones)" << std::endl;
}


void registrar_reproduccion(Cancion& cancion) {
    // TODO: suma 1 al campo reproducciones de la cancion recibida.
    // Al terminar, quien llamo la funcion debe ver el contador
    // actualizado sin necesidad de reasignar nada.
}


std::string clasificar_por_reproducciones(int reproducciones) {
    // TODO: retorna "Viral" si reproducciones >= 1000000,
    // "Popular" si esta entre 100000 y 999999,
    // "Emergente" si esta entre 10000 y 99999,
    // y "Nueva" en cualquier otro caso.
    return "Sin clasificar";
}


bool es_recomendable(int reproducciones, double calificacion) {
    // TODO: retorna true solo si reproducciones supera 50000
    // Y calificacion supera 4.0. En cualquier otro caso retorna false.
    return false;
}


std::string interpretar_calificacion(int calificacion_redondeada) {
    // TODO: usa un switch sobre calificacion_redondeada (1 a 5) y
    // retorna una etiqueta descriptiva para cada valor, por ejemplo
    // 5 -> "Excelente", 1 -> "Muy baja".
    return "Sin interpretar";
}
