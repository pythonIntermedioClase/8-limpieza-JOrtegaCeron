"""
main.py
Orquestador del pipeline de limpieza e integración — Sesión 8.

El estudiante construye este archivo sección a sección siguiendo la guía.
Cada opción del menú corresponde a una sección de sesion_08.md.
Si te bloqueas, puedes consultar la referencia en solucion/main.py.
"""

import os
import sys
from importlib import import_module

RAIZ = os.path.dirname(__file__)
SRC_DIR = os.path.join(RAIZ, "src")

for ruta in [RAIZ, SRC_DIR]:
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

import pandas as pd

data_loader = import_module("src.data_loader")
data_cleaner = import_module("src.data_cleaner")
api_client = import_module("src.api_client")
data_exporter = import_module("src.data_exporter")

cargar_datos = data_loader.cargar_datos
inspeccionar_estructura = data_loader.inspeccionar_estructura
contar_nulos = data_loader.contar_nulos
detectar_nulos_como_texto = data_loader.detectar_nulos_como_texto
contar_duplicados = data_loader.contar_duplicados
detectar_negativos = data_loader.detectar_negativos
generar_reporte_diagnostico = data_loader.generar_reporte_diagnostico

reemplazar_nulos_texto = data_cleaner.reemplazar_nulos_texto
eliminar_duplicados = data_cleaner.eliminar_duplicados
limpiar_texto = data_cleaner.limpiar_texto
corregir_fechas = data_cleaner.corregir_fechas
corregir_numericos = data_cleaner.corregir_numericos
filtrar_negativos = data_cleaner.filtrar_negativos

obtener_tasa_usd_cop = api_client.obtener_tasa_usd_cop
agregar_columna_cop = api_client.agregar_columna_cop

exportar_csv = data_exporter.exportar_csv
exportar_excel_multihoja = data_exporter.exportar_excel_multihoja


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

    ejecutando = True

    while ejecutando:
        print(MENU)
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            df_raw = cargar_datos(RUTA_DATOS)
            inspeccionar_estructura(df_raw)
            contar_nulos(df_raw)
            detectar_nulos_como_texto(df_raw)
            contar_duplicados(df_raw)
            detectar_negativos(df_raw, "activos_exterior_usd")
            reporte_diagnostico = generar_reporte_diagnostico(df_raw)
            print("=== Reporte de diagnóstico ===")
            print(reporte_diagnostico.to_string(index=False))

        elif opcion == "2":
            if df_raw is None:
                print("  ⚠  Primero diagnostica los datos con la opción 1.")
            else:
                df_sin_nas = reemplazar_nulos_texto(df_raw)
                df_sin_dupes, _ = eliminar_duplicados(df_sin_nas)
                df_texto_ok = limpiar_texto(df_sin_dupes, columnas=COLUMNAS_TEXTO)
                df_fechas_ok = corregir_fechas(df_texto_ok, "fecha_presentacion")

                df_nums_ok = df_fechas_ok.copy()
                for col in COLUMNAS_NUMERICAS:
                    df_nums_ok = corregir_numericos(df_nums_ok, col)

                df_limpio = filtrar_negativos(df_nums_ok, "activos_exterior_usd")
                print(f"  ✅  Limpieza completada. Filas resultantes: {len(df_limpio)}")
        
        elif opcion == "3":
            if df_limpio is None:
                print("  Debes ejecutar primero la opción 2 para limpiar los datos.")
            else:
                tasa_usd_cop = obtener_tasa_usd_cop()
                df_integrado = agregar_columna_cop(df_limpio, tasa_usd_cop)
                print("  Integración de tasa USD/COP completada.")

        elif opcion == "4":
            if df_integrado is None:
                print("  Debes ejecutar primero la opción 3 para integrar la API.")
            else:
                os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
                ruta_csv = os.path.join(CARPETA_RESULTADOS, "datos_limpios.csv")
                exportar_csv(df_integrado, ruta_csv)

                ruta_excel = os.path.join(CARPETA_RESULTADOS, "resultados.xlsx")
                exportar_excel_multihoja(
                    {
                        "Datos_limpios": df_integrado,
                        "Diagnostico": reporte_diagnostico,
                        "Resumen_limpieza": df_limpio,
                    },
                    ruta_excel,
                )
                print("  Resultados exportados correctamente.")

        elif opcion == "5":
            df_raw = cargar_datos(RUTA_DATOS)
            inspeccionar_estructura(df_raw)
            contar_nulos(df_raw)
            detectar_nulos_como_texto(df_raw)
            contar_duplicados(df_raw)
            detectar_negativos(df_raw, "activos_exterior_usd")
            reporte_diagnostico = generar_reporte_diagnostico(df_raw)

            df_limpio = df_raw.copy()
            df_limpio = reemplazar_nulos_texto(df_limpio, COLUMNAS_TEXTO)
            df_limpio = eliminar_duplicados(df_limpio)
            df_limpio = limpiar_texto(df_limpio, COLUMNAS_TEXTO)
            df_limpio = corregir_fechas(df_limpio)
            df_limpio = corregir_numericos(df_limpio, COLUMNAS_NUMERICAS)
            df_limpio = filtrar_negativos(df_limpio, ["activos_exterior_usd"])

            tasa_usd_cop = obtener_tasa_usd_cop()
            df_integrado = agregar_columna_cop(df_limpio, tasa_usd_cop)

            os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
            ruta_csv = os.path.join(CARPETA_RESULTADOS, "datos_limpios.csv")
            exportar_csv(df_integrado, ruta_csv)

            ruta_excel = os.path.join(CARPETA_RESULTADOS, "resultados.xlsx")
            exportar_excel_multihoja(
                {
                    "Datos_limpios": df_integrado,
                    "Diagnostico": reporte_diagnostico,
                    "Resumen_limpieza": df_limpio,
                },
                ruta_excel,
            )
            print("  Pipeline completo ejecutado.")

        elif opcion == "6":
            ejecutando = False

        else:
            print("  Opción no válida. Elige entre 1 y 6.")


if __name__ == "__main__":
    main()
