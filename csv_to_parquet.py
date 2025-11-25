import pandas as pd
from pathlib import Path

def convert_csv_to_parquet():

    # 1. Rutas: script (que YA es la raíz del repo) y carpeta RAW
    base_dir = Path(__file__).resolve().parent      # raíz del repo
    raw_dir = base_dir / "RAW"                      # PROYECTO.../RAW

    if not raw_dir.exists():
        print(f"Cree la carpeta: {raw_dir}")
        return

    # 2. Listar TODOS los .csv de RAW, excepto df_cambios.csv
    csv_files = [
    f for f in raw_dir.glob("*.csv")
    if f.name not in ("df_cambios.csv", "df_union_historico.csv")
    ]


    if not csv_files:
        print("No se encontraron archivos .csv para convertir")
        return

    # 3. Convertir cada .csv a .parquet en la MISMA carpeta RAW
    for csv_path in csv_files:
        parquet_path = csv_path.with_suffix(".parquet")

        try:
            print(f"Convirtiendo {csv_path.name} → {parquet_path.name} ...")
            df = pd.read_csv(csv_path, low_memory=False)
            df.to_parquet(parquet_path, index=False)
            print(f"Archivo generado: {parquet_path}")
        except Exception as e:
            print(f"Error al convertir {csv_path.name}: {e}")

if __name__ == "__main__":
    convert_csv_to_parquet()


