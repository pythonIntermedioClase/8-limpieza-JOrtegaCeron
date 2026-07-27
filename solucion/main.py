"""
main.py (solución de referencia)
Orquestador del pipeline de limpieza e integración — Sesión 8.

Cada opción del menú corresponde a una sección de sesion_08.md.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

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

RAIZ = os.path.dirname(os.path.dirname(__file__))
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


def construir_resumen_limpieza(df_raw, df_sin_dupes, df_fechas_ok,
                               df_limpio, df_integrado, tasa):
    """
    Construye el DataFrame que resume qué operación se aplicó y a cuántas filas.

    Args:
        df_raw (pd.DataFrame): Datos crudos, antes de limpiar.
        df_sin_dupes (pd.DataFrame): Datos tras eliminar duplicados.
        df_fechas_ok (pd.DataFrame): Datos tras corregir fechas.
        df_limpio (pd.DataFrame): Datos tras marcar negativos.
        df_integrado (pd.DataFrame): Datos con la columna COP agregada.
        tasa (float): Tasa USD/COP aplicada.

    Returns:
        pd.DataFrame: Tabla con columnas operacion y filas_afectadas.

    Examples:
        resumen = construir_resumen_limpieza(...)
        resumen.shape   -> (6, 2)
    """
    variantes = ["ninguno", "ND", "Sin dato"]
    filas = [
        {"operacion": "Reemplazar variantes no estándar -> NaN",
         "filas_afectadas": int(df_raw.isin(variantes).sum().sum())},
        {"operacion": "Eliminar duplicados exactos",
         "filas_afectadas": int(df_raw.duplicated().sum())},
        {"operacion": "Limpiar texto: tipo_persona, municipio",
         "filas_afectadas": len(df_sin_dupes)},
        {"operacion": "Corregir fechas: fecha_presentacion",
         "filas_afectadas": int(df_fechas_ok["fecha_presentacion"].isna().sum())},
        {"operacion": "Marcar negativos: activos_exterior_usd",
         "filas_afectadas": int(df_limpio["activos_exterior_usd_es_negativo"].sum())},
        {"operacion": f"Agregar columna COP (tasa: {tasa:.2f})",
         "filas_afectadas": int(df_integrado["activos_exterior_usd_cop"].notna().sum())},
    ]
    return pd.DataFrame(filas)


def ejecutar_pipeline_completo():
    """
    Ejecuta todo el flujo sin intervención y exporta el Excel de tres hojas.

    Returns:
        None
    """
    df_raw = cargar_datos(RUTA_DATOS)
    reporte_diagnostico = generar_reporte_diagnostico(df_raw)

    df_sin_nas = reemplazar_nulos_texto(df_raw)
    df_sin_dupes, _ = eliminar_duplicados(df_sin_nas)
    df_texto_ok = limpiar_texto(df_sin_dupes, columnas=COLUMNAS_TEXTO)
    df_fechas_ok = corregir_fechas(df_texto_ok, "fecha_presentacion")

    df_nums_ok = df_fechas_ok.copy()
    for col in COLUMNAS_NUMERICAS:
        df_nums_ok = corregir_numericos(df_nums_ok, col)

    df_limpio = filtrar_negativos(df_nums_ok, "activos_exterior_usd")

    tasa = obtener_tasa_usd_cop()
    df_integrado = agregar_columna_cop(df_limpio, "activos_exterior_usd", tasa)

    resumen_limpieza = construir_resumen_limpieza(
        df_raw, df_sin_dupes, df_fechas_ok, df_limpio, df_integrado, tasa
    )

    exportar_csv(df_integrado, CARPETA_RESULTADOS, "declaraciones_limpias")
    hojas = {
        "Datos_limpios": df_integrado,
        "Diagnostico": reporte_diagnostico,
        "Resumen_limpieza": resumen_limpieza,
    }
    exportar_excel_multihoja(hojas, CARPETA_RESULTADOS, "sesion08")
    print(f"Pipeline completo. Archivos en {CARPETA_RESULTADOS}")


def main():
    """
    Bucle principal del menú interactivo.

    Returns:
        None
    """
    df_raw = None
    df_limpio = None
    df_integrado = None
    reporte_diagnostico = None

    ejecutando = True
    while ejecutando:
        print(MENU)
        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            df_raw = cargar_datos(RUTA_DATOS)
            inspeccionar_estructura(df_raw)
            contar_nulos(df_raw)
            detectar_nulos_como_texto(df_raw)
            contar_duplicados(df_raw)
            detectar_negativos(df_raw, "activos_exterior_usd")
            reporte_diagnostico = generar_reporte_diagnostico(df_raw)
            print("\n=== Reporte de diagnóstico ===")
            print(reporte_diagnostico.to_string(index=False))

        elif opcion == "2":
            if df_raw is None:
                print("  Primero diagnostica los datos con la opción 1.")
            else:
                df_sin_nas = reemplazar_nulos_texto(df_raw)
                df_sin_dupes, _ = eliminar_duplicados(df_sin_nas)
                df_texto_ok = limpiar_texto(df_sin_dupes, columnas=COLUMNAS_TEXTO)
                df_fechas_ok = corregir_fechas(df_texto_ok, "fecha_presentacion")

                df_nums_ok = df_fechas_ok.copy()
                for col in COLUMNAS_NUMERICAS:
                    df_nums_ok = corregir_numericos(df_nums_ok, col)

                df_limpio = filtrar_negativos(df_nums_ok, "activos_exterior_usd")
                print(f"  Limpieza completada. Filas resultantes: {len(df_limpio)}")

        elif opcion == "3":
            if df_limpio is None:
                print("  Primero limpia los datos con la opción 2.")
            else:
                tasa = obtener_tasa_usd_cop()
                df_integrado = agregar_columna_cop(
                    df_limpio, "activos_exterior_usd", tasa
                )
                print(f"  Tasa USD/COP aplicada: {tasa:,.2f}")
                print(df_integrado[["nit", "activos_exterior_usd",
                                    "activos_exterior_usd_cop"]].head(5))

        elif opcion == "4":
            if df_integrado is None:
                print("  Primero integra los datos con la opción 3.")
            else:
                exportar_csv(df_integrado, CARPETA_RESULTADOS,
                             "declaraciones_limpias")
                hojas = {
                    "Datos_limpios": df_integrado,
                    "Diagnostico": reporte_diagnostico,
                }
                exportar_excel_multihoja(hojas, CARPETA_RESULTADOS, "sesion08")
                print(f"  Archivos generados en {CARPETA_RESULTADOS}")

        elif opcion == "5":
            ejecutar_pipeline_completo()

        elif opcion == "6":
            ejecutando = False

        else:
            print("  Opción no válida. Elige entre 1 y 6.")


if __name__ == "__main__":
    main()
