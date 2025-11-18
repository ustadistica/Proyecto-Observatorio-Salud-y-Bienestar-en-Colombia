from pathlib import Path
import pandas as pd

def main():
    # 1. Rutas: script, raíz del repo y carpeta RAW
    script_dir = Path(__file__).resolve().parent      # notebooks/
    base_dir = script_dir.parent                      # raíz del repo
    raw_dir = base_dir / "RAW"                        # carpeta RAW

    print(f"Directorio del script: {script_dir}")
    print(f"Carpeta RAW: {raw_dir}")

    if not raw_dir.exists():
        raise FileNotFoundError("No se encontró la carpeta 'RAW' al lado de 'notebooks'.")

    # 2. Listar todos los .parquet de RAW, omitiendo df_cambios.parquet
    archivos_parquet = [
        f for f in raw_dir.glob("*.parquet")
        if f.name != "df_cambios.parquet"
    ]

    print(f"Encontrados {len(archivos_parquet)} archivos .parquet en RAW (sin df_cambios.parquet).")

    if not archivos_parquet:
        print("No hay archivos .parquet para procesar. Fin.")
        return

    # 3. Procesar cada parquet
    for ruta_archivo in archivos_parquet:
        print("\n============================================================")
        print(f"📂 Procesando archivo: {ruta_archivo}")
        print("============================================================\n")

        # 3.1 Cargar el parquet
        df_union = pd.read_parquet(ruta_archivo)

        # 3.2 Información de tamaño
        print("════════════════════════════════════════════")
        print("📏 TAMAÑO DEL DATAFRAME")
        print(f"Filas: {df_union.shape[0]:,}")
        print(f"Columnas: {df_union.shape[1]:,}")

        # 3.3 Tipos de dato
        print("\n════════════════════════════════════════════")
        print("🔠 TIPOS DE DATO POR COLUMNA")
        print(df_union.dtypes)

        # 3.4 Valores únicos por columna
        print("\n════════════════════════════════════════════")
        print("🔎 VALORES ÚNICOS POR COLUMNA (con máximo 50 mostrados)")

        for col in df_union.columns:
            serie = df_union[col]
            nunique = serie.nunique(dropna=False)

            print("\n────────────────────────────────────────────")
            print(f"📌 Columna: {col}")
            print(f"🔢 Cantidad de valores únicos (incluyendo NaN): {nunique}")

            if nunique <= 50:
                print("Valores únicos:")
                print(serie.unique())
            else:
                print("Hay muchos valores únicos, se muestran solo los primeros 50:")
                print(pd.Series(serie.unique()).head(50))

        # 3.5 Eliminar columnas y guardar de nuevo el parquet
        print("\n════════════════════════════════════════════")
        print("🧹 ELIMINANDO COLUMNAS Y ACTUALIZANDO ARCHIVO")

        columnas_a_eliminar = ["id_fecha", "hash_sha256_num", "tps_nvl_ssb_id"]
        columnas_existentes = [c for c in columnas_a_eliminar if c in df_union.columns]

        if columnas_existentes:
            df_union = df_union.drop(columns=columnas_existentes)
            print(f"Columnas eliminadas: {columnas_existentes}")
        else:
            print("Ninguna de las columnas a eliminar existe en el DataFrame.")

        # Guardar sobre el mismo archivo parquet
        df_union.to_parquet(ruta_archivo, index=False)
        print(f"💾 Archivo parquet actualizado guardado en: {ruta_archivo}")

    print("\n✅ Procesamiento completado para todos los archivos.")

if __name__ == "__main__":
    main()
