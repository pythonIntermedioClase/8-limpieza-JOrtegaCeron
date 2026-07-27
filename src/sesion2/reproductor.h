// src/sesion2/reproductor.h
#pragma once

#include <string>
#include <vector>

// Representa una cancion del catalogo de Sonora.
struct Cancion {
    std::string titulo;
    std::string artista;
    std::string genero;
    int duracion_segundos;
    int reproducciones;
    double calificacion;
};

/**
 * Imprime los datos principales de una cancion en una sola linea.
 *
 * @param cancion Cancion a mostrar.
 */
void mostrar_cancion(const Cancion& cancion);

/**
 * Suma una reproduccion al contador de la cancion recibida.
 *
 * Modifica directamente la cancion original: quien llama esta funcion
 * ve el contador actualizado sin necesidad de reasignar nada.
 *
 * @param cancion Cancion cuyo contador de reproducciones se incrementa.
 */
void registrar_reproduccion(Cancion& cancion);

/**
 * Clasifica una cancion segun su numero de reproducciones.
 *
 * @param reproducciones Numero de reproducciones acumuladas.
 * @return "Viral", "Popular", "Emergente" o "Nueva" segun el rango.
 */
std::string clasificar_por_reproducciones(int reproducciones);

/**
 * Determina si una cancion es recomendable para la portada de Sonora.
 *
 * Una cancion es recomendable si supera el umbral de reproducciones
 * Y tiene una calificacion por encima del umbral minimo.
 *
 * @param reproducciones Numero de reproducciones acumuladas.
 * @param calificacion Calificacion promedio de los oyentes (0.0 a 5.0).
 * @return true si cumple ambas condiciones, false en caso contrario.
 */
bool es_recomendable(int reproducciones, double calificacion);

/**
 * Traduce una calificacion entera de 1 a 5 en una etiqueta descriptiva.
 *
 * @param calificacion_redondeada Calificacion redondeada al entero mas
 *        cercano (1 a 5).
 * @return Etiqueta textual asociada a esa calificacion.
 */
std::string interpretar_calificacion(int calificacion_redondeada);
