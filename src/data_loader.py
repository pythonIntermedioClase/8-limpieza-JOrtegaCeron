"""
data_loader.py
Funciones de carga e inspección inicial de datos para el pipeline de limpieza.
"""

import os

import pandas as pd
import numpy as np


def cargar_datos(ruta):
    """
    Carga un archivo CSV con todas las columnas como texto (dtype=str).

    Cargar con dtype=str evita que pandas infiera tipos y oculte problemas
    (por ejemplo, convertir un NIT como "900123456-1" a entero y perder el
    guion y el dígito de verificación).

    Args:
        ruta (str): Ruta al archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con todas las columnas de tipo object.

    Examples:
        df = cargar_datos("data/inputs/declaraciones_dirty.csv")
        df["nit"].dtype   -> dtype('O')   # object (texto), no int64
    """
    df = pd.read_csv(ruta, dtype=str)
    print(f"  Archivo cargado: {ruta}")
    print(f"  Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    return df


def inspeccionar_estructura(df):
    """
    Imprime las dimensiones del DataFrame y el tipo de dato de cada columna.

    Es un procedimiento: imprime en pantalla y no retorna ningún valor.

    Args:
        df (pd.DataFrame): DataFrame a inspeccionar.

    Returns:
        None

    Examples:
        inspeccionar_estructura(df)
        # === Estructura del DataFrame ===
        # Filas: 200  |  Columnas: 13
        # ...
    """
    print("\n=== Estructura del DataFrame ===")
    print(f"Filas: {df.shape[0]}  |  Columnas: {df.shape[1]}")
    print("\nTipos de dato por columna:")
    print(df.dtypes.to_string())


def contar_nulos(df):
    """
    Cuenta los valores NaN reales por columna e imprime el resultado.

    Solo detecta nulos reales (NaN). Las variantes de texto como "ninguno"
    o "ND" no las ve isnull(); para esas se usa detectar_nulos_como_texto().

    Args:
        df (pd.DataFrame): DataFrame a evaluar.

    Returns:
        pd.Series: Conteo de NaN por columna (todas las columnas).

    Examples:
        nulos = contar_nulos(df)
        nulos["saldo_favor"]   -> 21
    """
    nulos = df.isnull().sum()
    nulos_con_valor = nulos[nulos > 0]
    print("\n=== Nulos (NaN) por columna ===")
    if nulos_con_valor.empty:
        print("  Sin nulos detectados.")
    else:
        print(nulos_con_valor.to_string())
    return nulos


def detectar_nulos_como_texto(
    df,
    valores=["N/A", "NA", "n/a", "null", "NULL", "ninguno", ""],
):
    """
    Cuenta las celdas que contienen alguna de las cadenas indicadas como
    representación de dato faltante (nulos "disfrazados" de texto).

    No modifica el DataFrame: solo cuenta. pandas ya convirtió a NaN al cargar
    las variantes estándar ("N/A", "NA", "null", ""), así que aquí normalmente
    aparecen únicamente las variantes no estándar como "ninguno".

    Args:
        df (pd.DataFrame): DataFrame a evaluar.
        valores (list[str]): Cadenas que representan nulos textuales.

    Returns:
        pd.Series: Conteo de celdas afectadas por columna (todas las columnas).

    Examples:
        conteo = detectar_nulos_como_texto(df)
        conteo["saldo_favor"]   -> 4   # las 4 celdas con "ninguno"
    """
    mascara = df.isin(valores)
    conteo = mascara.sum()
    conteo_con_valor = conteo[conteo > 0]
    print(f"\n=== Nulos como texto {valores} por columna ===")
    if conteo_con_valor.empty:
        print("  No se encontró ninguna variante en ninguna columna.")
    else:
        print(conteo_con_valor.to_string())
    return conteo


def contar_duplicados(df):
    """
    Cuenta las filas duplicadas exactas e imprime tres ejemplos si existen.

    Args:
        df (pd.DataFrame): DataFrame a evaluar.

    Returns:
        int: Número de filas duplicadas (sin contar la primera ocurrencia).

    Examples:
        contar_duplicados(df)   -> 15
    """
    n_dupes = int(df.duplicated().sum())
    print("\n=== Duplicados exactos ===")
    print(f"  Filas duplicadas: {n_dupes}")
    if n_dupes > 0:
        print("  Ejemplos (primeros 3):")
        print(df[df.duplicated(keep=False)].head(3).to_string())
    return n_dupes


def detectar_negativos(df, columna):
    """
    Cuenta los valores negativos en una columna numérica que llega como texto.

    Convierte la columna a número con errors="coerce" solo para contar; no
    modifica el DataFrame original.

    Args:
        df (pd.DataFrame): DataFrame a evaluar.
        columna (str): Nombre de la columna a evaluar.

    Returns:
        int: Número de registros con valor negativo en esa columna.

    Examples:
        detectar_negativos(df, "activos_exterior_usd")   -> 8
    """
    serie_num = pd.to_numeric(df[columna], errors="coerce")
    n_negativos = int((serie_num < 0).sum())
    print(f"\n=== Valores negativos en '{columna}' ===")
    print(f"  Registros negativos: {n_negativos}")
    return n_negativos


def generar_reporte_diagnostico(
    df,
    valor_nulo_texto="ninguno",
    columna_negativos="activos_exterior_usd",
):
    """
    Ensambla un DataFrame con el resumen de todos los hallazgos de calidad.

    Consolida en una sola tabla lo que las funciones anteriores calculan por
    separado, para tener un inventario del estado del dato antes de limpiar.

    Args:
        df (pd.DataFrame): DataFrame a evaluar.
        valor_nulo_texto (str): Variante de nulo textual a contar. Por
            defecto "ninguno" (la variante no estándar de este dataset).
        columna_negativos (str): Columna en la que se cuentan los negativos.

    Returns:
        pd.DataFrame: Tabla con columnas: verificacion, resultado, detalle.

    Examples:
        reporte = generar_reporte_diagnostico(df)
        reporte.shape   -> (6, 3)
    """
    filas = []

    filas.append({
        "verificacion": "Total de filas",
        "resultado": len(df),
        "detalle": "Antes de cualquier limpieza",
    })

    n_dupes = int(df.duplicated().sum())
    filas.append({
        "verificacion": "Filas duplicadas exactas",
        "resultado": n_dupes,
        "detalle": "Eliminar con drop_duplicates()",
    })

    nulos_totales = int(df.isnull().sum().sum())
    filas.append({
        "verificacion": "Nulos reales (NaN) en todo el DataFrame",
        "resultado": nulos_totales,
        "detalle": "Detectados con isnull()",
    })

    nas_texto = int((df == valor_nulo_texto).sum().sum())
    filas.append({
        "verificacion": f'Celdas con texto "{valor_nulo_texto}"',
        "resultado": nas_texto,
        "detalle": "Reemplazar con np.nan antes de analizar nulos",
    })

    columna_fecha = df.get("fecha_presentacion", pd.Series(dtype=str))
    fechas_invalidas = int((columna_fecha == "01/01/1900").sum())
    filas.append({
        "verificacion": "Fechas '01/01/1900' en 'fecha_presentacion'",
        "resultado": fechas_invalidas,
        "detalle": "Reemplazar con NaT al corregir fechas",
    })

    columna_neg = df.get(columna_negativos, pd.Series(dtype=str))
    serie_num = pd.to_numeric(columna_neg, errors="coerce")
    n_negativos = int((serie_num < 0).sum())
    filas.append({
        "verificacion": f"Valores negativos en '{columna_negativos}'",
        "resultado": n_negativos,
        "detalle": "Marcar con columna booleana, no eliminar",
    })

    return pd.DataFrame(filas)


if __name__ == "__main__":
    # __file__ apunta a este archivo; subimos dos niveles para llegar a la raíz
    # del proyecto, sin importar desde qué directorio se ejecute.
    RAIZ = os.path.dirname(os.path.dirname(__file__))
    ruta = os.path.join(RAIZ, "data", "inputs", "declaraciones_dirty.csv")

    df = cargar_datos(ruta)
    inspeccionar_estructura(df)
    contar_nulos(df)
    detectar_nulos_como_texto(df)
    contar_duplicados(df)
    detectar_negativos(df, "activos_exterior_usd")

    reporte = generar_reporte_diagnostico(df)
    print("\n=== Reporte de diagnóstico consolidado ===")
    print(reporte.to_string(index=False))
