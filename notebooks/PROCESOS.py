# =============================================
# 1. Importar librerías necesarias
# =============================================
import pandas as pd
from google.colab import drive

# =============================================
# 2. Montar Google Drive para acceder a los archivos
# =============================================
drive.mount('/content/drive')

# =============================================
# 3. Cargar los archivos CSV de septiembre y octubre
# =============================================
df_sep = pd.read_csv('/content/drive/MyDrive/df_union sep.csv')
print("Dimensiones del DataFrame de septiembre:", df_sep.shape)
print(df_sep.head())

df_oct = pd.read_csv('/content/drive/MyDrive/df_union_oct.csv')
print("Dimensiones del DataFrame de octubre:", df_oct.shape)
print(df_oct.head(10))

# =============================================
# 4. Calcular el total de registros en cada DataFrame
# =============================================
total_sep = df_sep['Cantidad de registros'].sum()
print(f"El total de 'Cantidad de registros' en septiembre es: {total_sep}")

total_oct = df_oct['Cantidad de registros'].sum()
print(f"El total de 'Cantidad de registros' en octubre es: {total_oct}")

# =============================================
# 5. Renombrar columnas para distinguir los meses
# =============================================
df_sep = df_sep.rename(columns={'Cantidad de registros': 'df_registro_sep'})
df_oct = df_oct.rename(columns={'Cantidad de registros': 'df_registro_oct'})

display(df_sep.head())
display(df_oct.head())

# =============================================
# 6. Crear copias para uniones (septiembre y octubre)
# =============================================
sept = df_sep
octu = df_oct

# =============================================
# 7. Unir ambos DataFrames por la columna 'id_fecha'
# =============================================
dfs = sept.merge(octu, on="id_fecha", how="outer", suffixes=("_sept", "_oct"))

# =============================================
# 8. Calcular la diferencia entre registros de octubre y septiembre
# =============================================
dfs["diferencia"] = dfs["df_registro_oct"].fillna(0) - dfs["df_registro_sep"].fillna(0)

# Mostrar las primeras 100 filas de las columnas de interés
display(dfs[['df_registro_sep', 'df_registro_oct', 'diferencia']].head(100))

# =============================================
# 9. Guardar el resultado combinado en un nuevo CSV
# =============================================
dfs.to_csv('/content/drive/MyDrive/dfs_merged.csv', index=False)
print("Archivo 'dfs_merged.csv' guardado correctamente en tu Google Drive.")
