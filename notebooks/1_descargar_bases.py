###################################################################################################
from sodapy import Socrata
import pandas as pd
from datetime import datetime
from pathlib import Path
######################################################################################################

# CONTRIBUTIVO 
# 1. Conexión pública
client = Socrata("www.datos.gov.co", None)

# 2. ID del dataset
dataset_id = "tq4m-hmg2"

# 2.1 Consultar metadatos (para ver última actualización)
metadata = client.get_metadata(dataset_id)
fecha_actualizacion = metadata["rowsUpdatedAt"]  # timestamp en segundos
fecha_actualizacion = datetime.fromtimestamp(fecha_actualizacion).strftime("%Y-%m-%d %H:%M:%S")

print("📅 Fecha última actualización en datos.gov.co:", fecha_actualizacion)

# 3. Descargar toda la base con paginación
chunk_size = 100000000
offset = 0
all_data = []

while True:
    results = client.get(dataset_id, limit=chunk_size, offset=offset)
    if not results:
        break
    all_data.extend(results)
    offset += chunk_size
    print(f"Descargadas {offset} filas hasta ahora...")

# 4. Convertir a DataFrame
df = pd.DataFrame.from_records(all_data)

# 5. Agregar columna con la fecha de actualización
df["fecha_actualizacion"] = fecha_actualizacion

print("\n✅ Descarga completa")
print("Tamaño final:", df.shape)
print(df.head())

df.columns = ["Género","Grupo etario","Código de la entidad","Nombre de la entidad","Régimen","Tipo de afiliado","Estado del afiliado","Condición del beneficiario","Zona de Afiliación","Departamento","Municipio","tps_nvl_ssb_id","Nivel del Sisbén","Cantidad de registros","Fecha de actualización"]
df.head(10)

#############################################################################################################################################

# SUBSIDIADO 

# 1. Conexión a datos.gov.co (pública, sin token)
client2 = Socrata("www.datos.gov.co", None)

# 2. Definir ID del dataset (BDUA)
dataset_id = "d7a5-cnra"

# 2.1 Consultar metadatos (para ver última actualización)
metadata = client.get_metadata(dataset_id)
fecha_actualizacion = metadata["rowsUpdatedAt"]  # timestamp en segundos
fecha_actualizacion = datetime.fromtimestamp(fecha_actualizacion).strftime("%Y-%m-%d %H:%M:%S")

print("📅 Fecha última actualización en datos.gov.co:", fecha_actualizacion)

# 3. Descargar todos los registros usando paginación automática
chunk_size = 100000000   # número de filas por bloque (ajústalo según memoria disponible)
offset = 0
all_data = []

while True:
    # Descargar un bloque de datos
    results = client2.get(dataset_id, limit=chunk_size, offset=offset)

    # Si no llegan más filas, se detiene el bucle
    if not results:
        break

    all_data.extend(results)
    offset += chunk_size
    print(f"Descargadas {offset} filas hasta ahora...")

# 4. Convertir todo a DataFrame de pandas
df_bdua = pd.DataFrame.from_records(all_data)

# 5. Agregar columna con la fecha de actualización
df_bdua["fecha_actualizacion"] = fecha_actualizacion

print("\n✅ Descarga completa")
print("Tamaño final:", df_bdua.shape)
print(df_bdua.head())

df_bdua.columns= ["Género","Grupo etario","Código de la entidad","Nombre de la entidad","Régimen","Tipo de afiliado","Estado del afiliado","Condición del beneficiario","Zona de Afiliación","Departamento","Municipio","Nivel del Sisbén","Grupo poblacional del afiliado","Cantidad de registros","Fecha de actualización"]
df_bdua.head(10)

#######################################################################################################################################################################################

# UNIR LAS BASES 

df_union = pd.concat([df, df_bdua], axis=0, ignore_index=True)
df_union = df_union.fillna(0)
df_union.head(10)

# EXPORTAR LAS BASES 

# 1. Convertir "Fecha de actualización" a datetime
df_union["Fecha de actualización"] = pd.to_datetime(
    df_union["Fecha de actualización"],
    errors="coerce"
)

# 2. Tomar la fecha máxima
fecha_max = df_union["Fecha de actualización"].max()
print("Fecha máxima en 'Fecha de actualización':", fecha_max)

# 3. Formato año_mes, por ejemplo 2025_11
mes_anio = fecha_max.strftime("%Y_%m")

# 4. Construir ruta a RAW (subimos desde notebooks/ al root y entramos a RAW/)
script_dir = Path(__file__).resolve().parent   # carpeta notebooks/
base_dir = script_dir.parent                   # raíz del proyecto
raw_dir = base_dir / "RAW"

nombre_archivo = f"df_union_{mes_anio}.csv"
ruta_salida = raw_dir / nombre_archivo

# 6. Exportar df_union a CSV
df_union.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
print(f"✅ df_union exportado en: {ruta_salida}")