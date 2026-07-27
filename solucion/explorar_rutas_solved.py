import glob
import os
from pathlib import Path

# 1. Imprime el directorio de trabajo actual
print("CWD:", os.getcwd())

# 2. Construye la ruta al CSV usando os.path.join
ruta_csv = os.path.join("data", "inputs", "declaraciones_dirty.csv")
print("Ruta CSV:", ruta_csv)

# 3. Verifica si el archivo  "declaraciones_dirty.csv"
print("¿Existe?", os.path.exists(ruta_csv))

# 4. Imprime solo el nombre del archivo (sin carpetas)
print("Nombre:",os.path.basename(ruta_csv))

directorio =os.path.dirname(ruta_csv)
# 6. Lista todos los archivos CSV en data/inputs/ con os.listdir y filtra por extensión
ruta_csv = os.path.join(directorio,"*.csv")
csvs = glob.glob(ruta_csv)
print("CSVs encontrados:", csvs)