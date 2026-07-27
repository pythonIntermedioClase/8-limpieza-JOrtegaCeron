"""
main.py
Orquestador del pipeline de limpieza e integración — Sesión 8.

El estudiante construye este archivo sección a sección siguiendo la guía.
Cada opción del menú corresponde a una sección de sesion_08.md.
Si te bloqueas, puedes consultar la referencia en solucion/main.py.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pandas as pd
from data_loader import (
    cargar_datos, inspeccionar_estructura, contar_nulos,
    detectar_nulos_como_texto, contar_duplicados, detectar_negativos,
    generar_reporte_diagnostico,
)
from data_cleaner import (
    reemplazar_nulos_texto, eliminar_duplicados, limpiar_texto,
    corregir_fechas, corregir_numericos, filtrar_negativos,
)
from api_client import obtener_tasa_usd_cop, agregar_columna_cop
from data_exporter import exportar_csv, exportar_excel_multihoja


# --- Constantes del pipeline ---
# Se anclan a __file__ para que funcionen sin importar el directorio de trabajo.

RAIZ = os.path.dirname(__file__)
RUTA_DATOS = os.path.join(RAIZ, "data", "inputs", "declaraciones_dirty.csv")
CARPETA_RESULTADOS = os.path.join(RAIZ, "data", "outputs")
COLUMNAS_NUMERICAS = [
    "total_ingresos", "total_costos", "renta_liquida",
    "impuesto_cargo", "saldo_favor", "activos_exterior_usd",
]
COLUMNAS_TEXTO = ["tipo_persona", "municipio"]

MENU = """
==================================================================
   Sesión 8 - Limpieza e integración de fuentes externas
------------------------------------------------------------------
  1. Diagnosticar calidad de datos
  2. Limpiar datos
  3. Integrar tasa USD/COP desde API
  4. Exportar resultados
  5. Ejecutar pipeline completo
  6. Salir
==================================================================
"""


def main():
    # Variables de estado del pipeline. Se van llenando opción a opción.
    df_raw = None
    df_limpio = None
    df_integrado = None
    reporte_diagnostico = None

    # TODO (Sección 1): declara una variable booleana llamada `ejecutando`
    #       con valor True. El bucle principal usará esa variable como condición.

    # TODO (Sección 1): abre el bucle principal con `while ejecutando:`.
    #       Dentro del bucle:
    #       - imprime el menú con print(MENU)
    #       - lee la opción del usuario con input() y guárdala en `opcion`
    #       - agrega un bloque if/elif/else para enrutar cada opción

    # TODO (Sección 1): implementa la opción "1" — diagnóstico.
    #       Llama a las funciones de data_loader en secuencia:
    #       cargar_datos → inspeccionar_estructura → contar_nulos →
    #       detectar_nulos_como_texto → contar_duplicados → detectar_negativos →
    #       generar_reporte_diagnostico. Guarda el DataFrame en df_raw y
    #       el reporte en reporte_diagnostico.

    # TODO (Sección 2): implementa la opción "2" — limpieza.
    #       Encadena las funciones de data_cleaner sobre df_raw.
    #       Guarda el resultado en df_limpio.
    #       Muestra un aviso si df_raw es None (opción 1 no se ejecutó aún).

    # TODO (Sección 3): implementa la opción "3" — integración de API.
    #       Llama a obtener_tasa_usd_cop() y luego a agregar_columna_cop().
    #       Guarda el resultado en df_integrado.
    #       Muestra un aviso si df_limpio es None.

    # TODO (Sección 4): implementa la opción "4" — exportación.
    #       Llama a exportar_csv() y exportar_excel_multihoja() con las hojas
    #       Datos_limpios, Diagnostico y Resumen_limpieza.
    #       Muestra un aviso si df_integrado es None.

    # TODO (Sección 4): implementa la opción "5" — pipeline completo.
    #       Encadena todas las operaciones anteriores en secuencia, sin
    #       depender del estado acumulado de las opciones previas.

    # TODO (Sección 1): implementa la opción "6" — salida.
    #       Asigna False a `ejecutando` para terminar el bucle.

    # TODO (Sección 1): agrega el bloque else para opciones no válidas.
    #       Imprime un mensaje indicando que la opción no existe.
    pass


if __name__ == "__main__":
    main()
