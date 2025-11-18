from pathlib import Path
import pandas as pd

def main():
    # 1. Ruta del script y del repo
    script_dir = Path(__file__).resolve().parent      # notebooks/
    base_dir = script_dir.parent                      # raíz del repo
    raw_dir = base_dir / "RAW"                        # carpeta RAW

    print(f"Directorio del script: {script_dir}")
    print(f"Carpeta RAW: {raw_dir}")

    if not raw_dir.exists():
        raise FileNotFoundError("No se encontró la carpeta 'RAW' al lado de 'notebooks'.")

    # 2. Listar archivos .parquet en RAW (solo nivel actual)
    archivos_parquet = [
        f for f in raw_dir.glob("*.parquet")
        if f.name != "df_cambios.parquet"
    ]
    print(f"Encontrados {len(archivos_parquet)} archivos .parquet en RAW.")

    if not archivos_parquet:
        print("No hay archivos .parquet para unir. Fin.")
        return

    # 3. Leer y unir todos los parquet
    dfs = []
    for f in archivos_parquet:
        print(f"Leyendo: {f.name}")
        df_tmp = pd.read_parquet(f)
        dfs.append(df_tmp)

    df_union = pd.concat(dfs, ignore_index=False)

    #4. Descrpción del DataFrame unido

    print("Tamaño del DataFrame unido:")
    print(df_union.shape)

    print("Tipo de Columna del DataFrame unido:")
    print(df_union.dtypes)
    

    #5. Generar SHA256
    import hashlib

    # Columnas que NO deben participar en el hash
    columnas_omitir = ["Nombre de la entidad","Cantidad de registros", "Fecha de actualización"]

    # Columnas que SÍ se usan para el hash
    cols_para_hash = [c for c in df_union.columns if c not in columnas_omitir]

    def generar_sha256_num(fila):
        # Une todos los valores de la fila (solo de cols_para_hash) en un string
        fila_str = "|".join(str(x) for x in fila.values)
        # Devuelve el SHA256 como entero
        return int(hashlib.sha256(fila_str.encode("utf-8")).hexdigest(), 16)

    # Aplicar sobre las columnas seleccionadas
    df_union["hash_sha256_num"] = df_union[cols_para_hash].apply(
        generar_sha256_num,
        axis=1
    )

    # mover la columna al inicio
    cols = ["hash_sha256_num"] + [c for c in df_union.columns if c != "hash_sha256_num"]
    df_union = df_union[cols]

    #6. Descrpción del DataFrame con SHA256

    total_hashes = df_union["hash_sha256_num"].count()
    unicos_hashes = df_union["hash_sha256_num"].nunique()

    print(f"Total hashes generados: {total_hashes:,}")
    print(f"Hashes únicos: {unicos_hashes:,}")


    for col in df_union.columns:
        print(f"\n────────────────────────────────────────────")
        print(f"📌 Columna: {col}")
        print(df_union[col].unique())

    # devolver df_union si lo necesitas fuera
    return df_union

    salida = RAW / "df_union_historico.csv"
    df_union.to_csv(salida, index=False)
    print(f"✅ df_union final guardado en: {salida}")


#  ejecuta main()
if __name__ == "__main__":
    main()

 

