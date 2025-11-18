from pathlib import Path
import pandas as pd
from base_historico import main as construir_df_union
from datetime import datetime

def main():
    # Ejecuta el main del otro script y recibe el df_union final
    df_union = construir_df_union()

    # A partir de aquí trabajas con df_union
    print("Tamaño del DataFrame recibido:")
    print(df_union.shape)
    
    ### Constuir dataframe 

    df_union["Fecha de actualización"] =    pd.to_datetime(
        df_union["Fecha de actualización"],
        errors="coerce"   # si algo no se puede convertir, lo deja como NaT
    )
     
    # 3. Crear columna mes_año a partir de 'Fecha de actualización'
    df_union["mes_anio"] = df_union["Fecha de actualización"].dt.strftime("%Y_%m")


    # 4. Asegurar que 'Cantidad de registros' es numérica
    df_union["Cantidad de registros"] = pd.to_numeric(
        df_union["Cantidad de registros"],
        errors="coerce"
    ).fillna(0)

    # 5. Agrupar por hash y mes_año
    df_grouped = (
        df_union
        .groupby(["hash_sha256_num", "mes_anio"], as_index=False)["Cantidad de registros"]
        .sum()
    )

    # 6. Pivotear para construir df_cambios
    df_cambios = df_grouped.pivot(
        index="hash_sha256_num",
        columns="mes_anio",
        values="Cantidad de registros"
    ).fillna(0)

    print("\nTamaño de df_cambios:")
    print(df_cambios.shape)

    print("\nPrimeras filas de df_cambios:")
    print(df_cambios.head())    
    
    ### Generar columnas de cambios mes a mes

    # 1. Ordenar las columnas de mes_año
    meses = sorted(df_cambios.columns)  # ya que son 'YYYY_MM' esto funciona bien

    # 2. Para cada mes (desde el segundo), crear columna de cambios vs mes anterior
    for i in range(1, len(meses)):
        mes_actual = meses[i]
        mes_anterior = meses[i - 1]
    
        nueva_columna = f"{mes_actual}_cambios"
        df_cambios[nueva_columna] = df_cambios[mes_actual] - df_cambios[mes_anterior]

    # Si hay NaN porque falta algún valor, puedes rellenarlos con 0
    df_cambios = df_cambios.fillna(0)

    print("\n✅ Columnas de cambios generadas correctamente\n")
    print(df_cambios.head())

    df_cambios = df_cambios.reset_index()  
    
    ### Exportar df_cambios

    
  # Raíz del repositorio = carpeta que contiene RAW, notebooks, .gitignore, etc.
    repo_dir = Path(__file__).resolve().parent.parent
    raw_dir = repo_dir / "RAW"

    raw_dir.mkdir(exist_ok=True)

    ruta_salida = raw_dir / "df_cambios.csv"
    df_cambios.to_csv(ruta_salida, index=False)
    print(f"✅ df_cambios exportado en: {ruta_salida}")

    
    return df_union
   
if __name__ == "__main__":
    main()


   