"""
data_cleaner.py — ARCHIVO DE EJERCICIO
Funciones de limpieza y corrección de datos para el pipeline de la Sesión 8.

Cada función está SIN implementar. Tu tarea es escribir el cuerpo para que
cumpla lo descrito en su docstring (propósito, argumentos, retorno y "Casos a
resolver"). Los ejemplos muestran el comportamiento esperado, no la solución.

Guía de trabajo:
  - Implementa una función a la vez y pruébala en el bloque __main__.
  - Cada función debe RETORNAR un DataFrame nuevo, sin modificar el que recibe.
  - Referencia teórica: Sección 2 de sesion_08.md.
  - Solución de referencia (úsala solo si te bloqueas): solucion/data_cleaner.py
"""

import os
import sys

# data_loader completo vive en src/; lo importamos desde allí.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd
import numpy as np
from data_loader import cargar_datos


def reemplazar_nulos_texto(
    df,
    valores=["N/A", "NA", "n/a", "null", "NULL", "ninguno", ""],
):
    """
    Reemplaza por un nulo real (NaN) las celdas cuyo texto represente un dato
    faltante "disfrazado".

    Debe ejecutarse antes que el resto de la limpieza, porque las funciones que
    siguen asumen que los faltantes ya son NaN reales.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        valores (list[str]): Cadenas que representan nulos textuales.

    Returns:
        pd.DataFrame: DataFrame nuevo con esas celdas convertidas a NaN.

    Casos a resolver:
        - Cualquier celda, en cualquier columna, cuyo valor esté en `valores`
          debe quedar como NaN (no como el texto original).
        - Las celdas que ya eran NaN deben seguir siendo NaN.
        - El DataFrame original no debe modificarse.

    Examples:
        df["saldo_favor"].isnull().sum()   -> 21   # antes
        df = reemplazar_nulos_texto(df)
        df["saldo_favor"].isnull().sum()   -> 25   # tras convertir los "ninguno"
    """
    df = df.replace(valores, np.nan)
    return df
    
    # EJERCICIO: recorre el DataFrame y sustituye por un nulo real todas las
    #            celdas cuyo valor aparezca en `valores`. Devuelve un DataFrame
    #            nuevo (no modifiques el original). Al terminar, la detección de
    #            nulos debe "ver" esas celdas como faltantes.
    raise NotImplementedError("Implementa reemplazar_nulos_texto()")


def eliminar_duplicados(df):
    """
    Elimina filas duplicadas exactas conservando la primera ocurrencia.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.

    Returns:
        tuple[pd.DataFrame, int]: DataFrame sin duplicados y número de filas
        eliminadas.

    Casos a resolver:
        - Solo se eliminan filas idénticas en TODAS sus columnas.
        - Se conserva la primera aparición de cada fila.
        - Debes informar cuántas filas se eliminaron (compara el tamaño antes
          y después).

    Examples:
        df, n = eliminar_duplicados(df)
        n   -> 15
        len(df)  # baja de 200 a 185
    """
    # EJERCICIO: produce un DataFrame sin filas repetidas y calcula cuántas
    #            desaparecieron. Retorna la tupla (df_sin_duplicados, eliminadas).
    filas_antes = len(df)
    df = df.drop_duplicates()
    eliminadas = filas_antes - len(df)
    print(f"  Duplicados eliminados: {eliminadas}")
    return df, eliminadas


def limpiar_texto(df, columnas):
    """
    Normaliza columnas de texto: sin espacios al inicio/final y en minúsculas.

    Sirve para unificar variantes que solo difieren por espacios o mayúsculas,
    de modo que un agrupamiento no las trate como categorías distintas.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columnas (list[str]): Nombres de columnas de texto a normalizar.

    Returns:
        pd.DataFrame: DataFrame nuevo con esas columnas normalizadas.

    Casos a resolver:
        - " Natural", "NATURAL" y "natural" deben quedar todas como "natural".
        - Solo se tocan las columnas indicadas en `columnas`.
        - El DataFrame original no debe modificarse.

    Examples:
        df = limpiar_texto(df, columnas=["tipo_persona"])
        sorted(df["tipo_persona"].unique())   -> ['juridica', 'natural']
    """
    # EJERCICIO: para cada columna indicada, quita los espacios laterales de
    #            cada celda y pásala a minúsculas. Trabaja sobre una copia y
    #            devuélvela.
    df = df.copy()
    for columna in columnas:
        df[columna] = df[columna].str.strip().str.lower()
    return df


def corregir_fechas(df, columna):
    """
    Convierte una columna de texto a tipo fecha (datetime), dejando como fecha
    nula (NaT) lo que no sea una fecha válida o real.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columna (str): Nombre de la columna con fechas en texto.

    Returns:
        pd.DataFrame: DataFrame nuevo con la columna convertida a datetime.

    Casos a resolver:
        - La columna trae DOS formatos mezclados que deben convertirse bien:
          uno tipo "18/06/2024" (día/mes/año, formato colombiano) y otro tipo
          "Jun 18 2024" (mes en inglés). Ninguno de los dos debe perderse.
        - Los valores imposibles de interpretar como fecha (por ejemplo
          "sin fecha" o "32/13/2024") deben quedar como fecha nula, sin
          detener el programa con una excepción.
        - La fecha centinela "01/01/1900" representa "fecha desconocida" en el
          sistema de origen y también debe quedar como fecha nula.
        - Pista de contexto: en pandas moderno, convertir una columna con
          formatos mezclados requiere pedir explícitamente ese comportamiento;
          investiga en la Sección 2 de la guía por qué y cómo.

    Examples:
        df = corregir_fechas(df, "fecha_presentacion")
        df["fecha_presentacion"].isna().sum()   -> 8   # 5 centinela + 3 ilegibles
    """
    # EJERCICIO: convierte la columna de texto a fecha manejando los tres casos
    #            descritos arriba (formatos mezclados, valores ilegibles y la
    #            fecha centinela 01/01/1900). Trabaja sobre una copia.
    raise NotImplementedError("Implementa corregir_fechas()")


def corregir_numericos(df, columna):
    """
    Convierte una columna de texto a número (float), dejando como nulo lo que
    no se pueda interpretar como número.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columna (str): Nombre de la columna a convertir.

    Returns:
        pd.DataFrame: DataFrame nuevo con la columna convertida a número.

    Casos a resolver:
        - Los valores numéricos en texto ("18444927") deben quedar como número.
        - Los valores no convertibles (vacíos, texto no numérico) deben quedar
          como nulo, sin lanzar excepción.
        - El DataFrame original no debe modificarse.

    Examples:
        df["total_ingresos"].dtype   # antes: texto (object)
        df = corregir_numericos(df, "total_ingresos")
        df["total_ingresos"].dtype   # después: float
    """
    # EJERCICIO: convierte la columna a número tolerando valores no convertibles
    #            (que deben quedar como nulo). Trabaja sobre una copia.
    raise NotImplementedError("Implementa corregir_numericos()")


def filtrar_negativos(df, columna):
    """
    Marca los valores negativos con una columna booleana, SIN eliminar filas.

    Un negativo puede ser un error de digitación o tener explicación de negocio;
    por eso no se borra, se marca para revisión.

    Args:
        df (pd.DataFrame): DataFrame a evaluar.
        columna (str): Nombre de la columna numérica a evaluar.

    Returns:
        pd.DataFrame: DataFrame nuevo con la columna f"{columna}_es_negativo"
        de tipo booleano.

    Casos a resolver:
        - La nueva columna debe llamarse exactamente f"{columna}_es_negativo".
        - Debe valer True donde el valor es menor que cero y False en el resto.
        - No se elimina ninguna fila.

    Examples:
        df = filtrar_negativos(df, "activos_exterior_usd")
        df["activos_exterior_usd_es_negativo"].sum()   -> 8
    """
    # EJERCICIO: agrega la columna booleana descrita, marcando los negativos.
    #            No elimines filas. Trabaja sobre una copia.
    raise NotImplementedError("Implementa filtrar_negativos()")


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(__file__))
    ruta = os.path.join(RAIZ, "data", "inputs", "declaraciones_dirty.csv")
    df = cargar_datos(ruta)

    # A medida que implementes cada función, esta secuencia debería correr
    # completa. Antes de implementarlas, cada llamada lanzará NotImplementedError.
    print(f"Filas iniciales: {len(df)}")

    df = reemplazar_nulos_texto(df)
    print(df["saldo_favor"].value_counts(dropna=False).head())
    df, eliminadas = eliminar_duplicados(df)
    print(f"Filas después de eliminar duplicados: {len(df)}")
    print(f"Eliminadas: {eliminadas}")
    df = limpiar_texto(df, columnas=["tipo_persona", "municipio"])
    print(df["tipo_persona"].value_counts())
    df = corregir_fechas(df, "fecha_presentacion")

    columnas_numericas = [
        "total_ingresos", "total_costos", "renta_liquida",
        "impuesto_cargo", "saldo_favor", "activos_exterior_usd",
    ]
    for col in columnas_numericas:
        df = corregir_numericos(df, col)

    df = filtrar_negativos(df, "activos_exterior_usd")

    print(f"Filas finales: {len(df)}")
    print(f"Tipos resultantes:\n{df.dtypes.to_string()}")
