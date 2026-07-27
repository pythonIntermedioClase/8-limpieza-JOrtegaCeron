"""
data_exporter.py — ARCHIVO DE EJERCICIO
Exportación de DataFrames a CSV y a Excel con múltiples hojas.

Nota: en el material del curso este módulo se entrega completo (Sección 4). Esta
es una versión de práctica opcional para que implementes tú las dos funciones
de exportación. Ambas están sin resolver.

Guía de trabajo:
  - Referencia teórica: Sección 4 de sesion_08.md.
  - Solución de referencia (úsala solo si te bloqueas): solucion/data_exporter.py
"""

import os
from datetime import date

import pandas as pd


def exportar_csv(df, carpeta, nombre_base):
    """
    Exporta un DataFrame a CSV incluyendo la fecha del día en el nombre.

    Args:
        df (pd.DataFrame): DataFrame a exportar.
        carpeta (str): Directorio de destino.
        nombre_base (str): Prefijo del archivo.

    Returns:
        str: Ruta completa del archivo generado.

    Casos a resolver:
        - Si la carpeta de destino no existe, debe crearse (sin fallar si ya
          existe).
        - El nombre del archivo debe ser "{nombre_base}_{YYYYMMDD}.csv", con la
          fecha de hoy.
        - El CSV se guarda sin la columna de índice y con codificación utf-8.
        - La función retorna la ruta completa del archivo creado.

    Examples:
        exportar_csv(df, "data/outputs", "declaraciones_limpias")
        # crea data/outputs/declaraciones_limpias_20260726.csv y retorna su ruta
    """
    # EJERCICIO: asegura que la carpeta exista, arma el nombre con la fecha de
    #            hoy, guarda el CSV (sin índice, utf-8) y retorna la ruta.
    raise NotImplementedError("Implementa exportar_csv()")


def exportar_excel_multihoja(hojas, carpeta, nombre_base):
    """
    Exporta varios DataFrames a un mismo archivo Excel, uno por hoja.

    Args:
        hojas (dict[str, pd.DataFrame]): Claves = nombres de hoja,
            valores = DataFrames. Ej: {"Datos_limpios": df1, "Diagnostico": df2}
        carpeta (str): Directorio de destino.
        nombre_base (str): Prefijo del archivo.

    Returns:
        str: Ruta completa del archivo generado.

    Casos a resolver:
        - Si la carpeta de destino no existe, debe crearse.
        - El nombre del archivo debe ser "{nombre_base}_{YYYYMMDD}.xlsx".
        - Cada entrada del diccionario `hojas` se escribe como una hoja distinta,
          usando la clave como nombre de la hoja, sin la columna de índice.
        - La función retorna la ruta completa del archivo creado.
        - Pista de contexto: para escribir varias hojas en un mismo archivo se
          usa un "escritor" de Excel; revisa la Sección 4 de la guía.

    Examples:
        exportar_excel_multihoja({"Datos_limpios": df}, "data/outputs", "sesion08")
        # crea data/outputs/sesion08_20260726.xlsx con una hoja "Datos_limpios"
    """
    # EJERCICIO: asegura la carpeta, arma el nombre con la fecha de hoy y escribe
    #            una hoja por cada entrada del diccionario (sin índice). Retorna
    #            la ruta.
    raise NotImplementedError("Implementa exportar_excel_multihoja()")


if __name__ == "__main__":
    df_prueba = pd.DataFrame({
        "nit": ["900123456-1", "800234568-0", "700345679-9"],
        "total_ingresos": [1_200_000, 3_450_000, 890_000],
        "fecha_presentacion": pd.to_datetime(
            ["2024-03-22", "2024-01-15", "2024-06-01"]
        ),
    })

    df_diagnostico = pd.DataFrame({
        "verificacion": ["Total filas", "Duplicados", "Nulos reales"],
        "resultado": [200, 15, 29],
        "detalle": ["Antes de limpieza", "Eliminar con drop_duplicates()", "isnull()"],
    })

    carpeta = os.path.join("data", "outputs")
    exportar_csv(df_prueba, carpeta, "prueba")
    exportar_excel_multihoja(
        {"Datos_limpios": df_prueba, "Diagnostico": df_diagnostico},
        carpeta,
        "prueba",
    )
