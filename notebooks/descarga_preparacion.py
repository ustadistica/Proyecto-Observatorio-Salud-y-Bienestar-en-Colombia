
from sodapy import Socrata
import pandas as pd
from datetime import datetime

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
chunk_size = 5000000
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


df.columns = ["Género","Grupo etario","Código de la entidad","Nombre de la entidad","Régimen","Tipo de afiliado","Estado del afiliado","Condición del beneficiario","Zona de Afiliación","Departamento","Municipio","Nivel del Sisbén","Cantidad de registros","tps_nvl_ssb_id","Fecha de actualización"]

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
chunk_size = 5000000   # número de filas por bloque (ajústalo según memoria disponible)
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

# UNIR LAS BASES 

df_union = pd.concat([df, df_bdua], axis=0, ignore_index=True)
df_union = df_union.fillna(0)

# SHA 256
import hashlib

# 1. Función para generar SHA256 en formato numérico
def generar_sha256_num(fila):
    fila_str = ''.join(str(x) for x in fila.values)
    # Convertimos a entero usando base 16
    return int(hashlib.sha256(fila_str.encode()).hexdigest(),16)


# 2. Aplicamos la función fila por fila y creamos la nueva columna
df_union["hash_sha256_num"] = df_union.apply(generar_sha256_num, axis=1)

cols = ["hash_sha256_num"] + [c for c in df_union.columns if c != "hash_sha256_num"]
df_union = df_union[cols]


# 3. Contar cuántos SHA256 son únicos
num_unicos = df_union["hash_sha256_num"].nunique()
num_total = len(df_union)

print(f"Total filas: {num_total}")
print(f"SHA256 únicos: {num_unicos}")
print(f"Repetidos: {num_total - num_unicos}")


df_union = df_union.drop_duplicates(subset=["hash_sha256_num"])

print("Shape after removing duplicates:", df_union.shape)
display(df_union.head())

df_union['id_fecha'] = df_union['hash_sha256_num'].astype(str) + "_" + df_union['Fecha de actualización'].astype(str)
display(df_union.head())


from google.colab import drive
# Montamos el Drive
drive.mount('/content/drive')


# Definir la ruta donde guardarás tu base final
ruta_guardado = "/content/drive/MyDrive/df_union_actualizado.csv"
# Guardar como CSV (se sobreescribe cada vez que corras el código)
df_union.to_csv(ruta_guardado, index=False, encoding="utf-8-sig")
print(f"Base guardada en: {ruta_guardado}")
