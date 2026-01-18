import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SILVER_PATH = BASE_DIR / "data" / "silver" / "solicitudes_clean.csv"
GOLD_FOLDER = BASE_DIR / "data" / "gold"
GOLD_FOLDER.mkdir(parents=True, exist_ok=True)
GOLD_PATH = GOLD_FOLDER / "kpis_servicio_ciudadano.csv"

# Paths Coolab
#SILVER_PATH = "/content/data/silver/solicitudes_clean.csv"
#GOLD_PATH = "/content/data/gold/kpis_servicio_ciudadano.csv"

# 2. Verificación de seguridad
if not SILVER_PATH.exists():
    print(f"❌ ERROR: No se encontró el archivo: {SILVER_PATH}")
    print("👉 Asegúrate de ejecutar primero: python pipelines/bronce_to_silver.py")
    exit()

# 3. Carga de datos (Ahora usará la ruta correcta en C:\Users\MR\...)
print(f"📂 Cargando datos desde: {SILVER_PATH}")
df = pd.read_csv(SILVER_PATH, parse_dates=["created_at", "closed_at"])

# -------------------------
# 1. Derivar periodo
# -------------------------
df["period_year"] = df["created_at"].dt.year
df["period_month"] = df["created_at"].dt.month
df["period_start"] = df["created_at"].dt.to_period("M").dt.to_timestamp()

# -------------------------
# 2. Flags para KPIs
# -------------------------
df["is_closed"] = df["status"] == "cerrado"
df["is_cancelled"] = df["status"] == "anulado"
df["is_digital"] = df["channel"].isin(["web", "app", "email"])

# -------------------------
# 3. Agregación por oficina + mes
# -------------------------
gold = df.groupby(
    ["office_id", "period_year", "period_month", "period_start"],
    as_index=False
).agg(
    total_requests=("request_id", "count"),
    closed_requests=("is_closed", "sum"),
    cancelled_requests=("is_cancelled", "sum"),
    digital_requests=("is_digital", "sum"),
    avg_resolution_hours=("resolution_hours", "mean"),
    avg_cost_soles=("cost_soles", "mean"),
    avg_satisfaction=("satisfaction_rating", "mean")
)

# -------------------------
# 4. KPIs porcentuales
# -------------------------
gold["pct_closed"] = (gold["closed_requests"] / gold["total_requests"]) * 100
gold["pct_cancelled"] = (gold["cancelled_requests"] / gold["total_requests"]) * 100
gold["pct_digital"] = (gold["digital_requests"] / gold["total_requests"]) * 100

# -------------------------
# 5. Categoría más frecuente
# -------------------------
top_category = (
    df.groupby(["office_id", "period_year", "period_month", "category"])
      .size()
      .reset_index(name="category_count")
      .sort_values(
          ["office_id", "period_year", "period_month", "category_count"],
          ascending=False
      )
      .drop_duplicates(["office_id", "period_year", "period_month"])
)

gold = gold.merge(
    top_category,
    on=["office_id", "period_year", "period_month"],
    how="left"
)

gold.rename(columns={"category": "top_category"}, inplace=True)

# -------------------------
# 6. Formato final
# -------------------------
numeric_cols = [
    "avg_resolution_hours", "avg_cost_soles", "avg_satisfaction",
    "pct_closed", "pct_cancelled", "pct_digital"
]

gold[numeric_cols] = gold[numeric_cols].round(2)

# -------------------------
# 7. Guardar Gold
# -------------------------
gold.to_csv(GOLD_PATH, index=False)

print("✅ Capa Gold generada correctamente")
print(f"Archivo: {GOLD_PATH}")
