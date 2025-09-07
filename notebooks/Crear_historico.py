# actualiza_hist_df_union.py
# -- coding: utf-8 --
import pandas as pd
import runpy
from pathlib import Path

# === Configuración ===
SCRIPT_PATH = Path(__file__).resolve().parent / "notebooks" / "descarga_preparacion.py"
OUT_CSV = Path("df_union_history.csv")          # archivo histórico en la misma carpeta
KEY_COL = "id_fecha"                            # columna llave

# === Ejecutar el script fuente para obtener df_union ===
ns = runpy.run_path(str(SCRIPT_PATH))
if "df_union" not in ns:
    raise KeyError("El script 'descarga_preparacion.py' no definió una variable df_union.")

df_union = ns["df_union"]
if not isinstance(df_union, pd.DataFrame):
    raise TypeError("df_union debe ser un pandas.DataFrame")

if KEY_COL not in df_union.columns:
    raise KeyError(f"La columna {KEY_COL} no existe en df_union. Columnas: {list(df_union.columns)}")

# === Deduplicar dentro del lote nuevo ===
df_new = df_union.drop_duplicates(subset=[KEY_COL]).copy()

# === Cargar histórico existente si lo hay ===
if OUT_CSV.exists():
    df_hist = pd.read_csv(OUT_CSV)

    if KEY_COL not in df_hist.columns:
        raise KeyError(f"La columna {KEY_COL} no existe en el histórico {OUT_CSV}")

    # Unir y deduplicar
    common_cols = sorted(set(df_hist.columns).union(df_new.columns))
    df_hist = df_hist.reindex(columns=common_cols)
    df_new = df_new.reindex(columns=common_cols)

    df_out = pd.concat([df_hist, df_new], ignore_index=True)
    df_out = df_out.drop_duplicates(subset=[KEY_COL], keep="last")
else:
    df_out = df_new

# === Ordenar y guardar CSV ===
df_out = df_out.sort_values(by=[KEY_COL]).reset_index(drop=True)
df_out.to_csv(OUT_CSV, index=False)

print(f"Histórico actualizado en: {OUT_CSV.resolve()}")
print(f"Filas totales: {len(df_out)} | Columnas: {len(df_out.columns)}")