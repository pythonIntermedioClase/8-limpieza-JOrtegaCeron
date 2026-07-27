// src/sesion2/main.cpp
#include "reproductor.h"

#include <iostream>
#include <vector>

int main() {
    std::vector<Cancion> catalogo = {
        {"La Gota Fria", "Carlos Vives", "Vallenato", 245, 1250000, 4.6},
        {"La Rebelion", "Joe Arroyo", "Salsa", 260, 82000, 4.2},
        {"Rio", "Bomba Estereo", "Electronica", 210, 15300, 3.8},
    };

    bool ejecutando = true;
    while (ejecutando) {
        std::cout << "\n=== Sonora ===\n";
        std::cout << "1. Mostrar catalogo\n";
        std::cout << "2. Registrar una reproduccion\n";
        std::cout << "3. Clasificar una cancion por reproducciones\n";
        std::cout << "4. Ver si una cancion es recomendable\n";
        std::cout << "5. Interpretar una calificacion (1 a 5)\n";
        std::cout << "6. Salir\n";
        std::cout << "Elige una opcion: ";

        int opcion = 0;
        std::cin >> opcion;

        switch (opcion) {
            case 1:
                for (const Cancion& cancion : catalogo) {
                    mostrar_cancion(cancion);
                }
                break;
            case 2:
                // TODO (Seccion 3, paso por referencia): llama
                // registrar_reproduccion(catalogo[0]) y muestra el
                // contador antes y despues para confirmar el cambio.
                break;
            case 3:
                // TODO (Seccion 4, condicionales): llama
                // clasificar_por_reproducciones(catalogo[0].reproducciones)
                // e imprime el resultado.
                break;
            case 4:
                // TODO (Seccion 5, operadores booleanos): llama
                // es_recomendable(catalogo[0].reproducciones,
                // catalogo[0].calificacion) e imprime el resultado.
                break;
            case 5:
                // TODO (Seccion 6, switch): pide al usuario una
                // calificacion entera y llama interpretar_calificacion().
                break;
            case 6:
                ejecutando = false;
                break;
            default:
                std::cout << "Opcion invalida.\n";
                break;
        }
    }

    std::cout << "Hasta pronto.\n";
    return 0;
}
