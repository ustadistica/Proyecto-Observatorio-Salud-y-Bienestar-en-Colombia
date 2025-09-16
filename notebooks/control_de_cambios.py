# En esta parte del código se hizo una copia de la base original 
# y se modificó la variable 'cantidad_registros' con el fin de 
# realizar el control de cambios. 
# El objetivo es identificar cuántas personas se movieron de 
# contributivo a subsidiado. 
# Estos son datos de prueba para validar el código, a la espera 
# de que lleguen los datos reales y poder confirmar que funciona correctamente.


import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/df_union.csv')
df.shape

total_original = df['Cantidad de registros'].sum()
print(f"El total de 'Cantidad de registros' es: {total_original}")


# en esta parte lo que se hizo fue guardar la base original en un data frame diferente para no dañar el original, este data frame si hixzo con el fin de alterar la cantidad de registos para poder hacer el control de cambios 
import pandas as pd
import random
df_arreglos = pd.read_csv('/content/drive/MyDrive/df_union.csv')

# Modifica cada fila aleatoriamente
for idx in df.index:
    cambio = random.randint(-5, 5)  # Cambia este rango según necesites
    df_arreglos.loc[idx, 'Cantidad de registros'] += cambio

# Ajusta valores negativos a cero
df_arreglos['Cantidad de registros'] = df_arreglos['Cantidad de registros'].clip(lower=0)

diferencia = total_original - df_arreglos['Cantidad de registros'].sum()
df.loc[df_arreglos.sample(n=1).index, 'Cantidad de registros'] += diferencia

df_arreglos.to_csv('/content/drive/MyDrive/df_union_modificado.csv', index=False)

df_arre = pd.read_csv('/content/drive/MyDrive/df_union_modificado.csv') 

total_cantidad_registros = df_arreglos['Cantidad de registros'].sum()
print(f"El total de 'Cantidad de registros' es: {total_cantidad_registros}")


#### en esta parte del código se cambiaron los nombres de las bases tanto original como el de la copia para poder mirar la diferencia en el control de cambios 
df = df.rename(columns={'Cantidad de registros': 'df_registro_sep'})
display(df.head())

df_arre = df_arre.rename(columns={'Cantidad de registros': 'df_registro_oct'})
display(df_arre.head())

## llame los data frame en sept y oct para poder mirar la diferencia, , "recuerde que el data frame de oct es la copia de la original base" 
sept = df
octu = df_arre

dfs = sept.merge(octu, on="id_fecha", how="outer", suffixes=("_sept", "_oct"))

# 3. Calcular la diferencia en registros
# ============================
dfs["diferencia"] = dfs["df_registro_oct"].fillna(0) - dfs["df_registro_sep"].fillna(0)
## asi seria la tabla de diferencia
display(dfs[['df_registro_sep', 'df_registro_oct','diferencia']].head(100))
