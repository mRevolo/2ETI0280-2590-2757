import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OFICINAS_PATH = BASE_DIR / "data" / "bronze" / "oficinas.csv"
SOLICITUDES_PATH = BASE_DIR / "data" / "bronze" / "solicitudes_ciudadanas.csv"
SILVER_FOLDER = BASE_DIR / "data" / "silver"
SILVER_FOLDER.mkdir(parents=True, exist_ok=True) # Crea la carpeta si no existe
SILVER_PATH = SILVER_FOLDER / "solicitudes_clean.csv"
LOG_PATH = SILVER_FOLDER / "data_quality_log.csv"

## Coolab:
##OFICINAS_PATH = "/content/data/bronze/oficinas.csv"
##SOLICITUDES_PATH = "/content/data/bronze/solicitudes_ciudadanas.csv"
##SILVER_PATH = "/content/data/silver/solicitudes_clean.csv"
##LOG_PATH = "/content/data/silver/data_quality_log.csv"

oficinas = pd.read_csv(OFICINAS_PATH)
df = pd.read_csv(SOLICITUDES_PATH)

log = {}
total_read = len(df)

# -------------------------
# 1. COMPLETITUD
# -------------------------
mandatory = ["request_id", "office_id", "created_at", "status", "category"]
missing = df[mandatory].isnull().any(axis=1).sum()
df = df.dropna(subset=mandatory)
log["missing_mandatory"] = missing

# -------------------------
# 2. UNICIDAD
# -------------------------
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
duplicates = df.duplicated("request_id").sum()

df = df.sort_values("created_at", ascending=False)
df = df.drop_duplicates("request_id", keep="first")
log["duplicates_removed"] = duplicates

# -------------------------
# 3. VALIDEZ request_id
# -------------------------
invalid_req = ~df["request_id"].str.match(r"^REQ-\d{4}$", na=False)
log["invalid_request_id"] = invalid_req.sum()
df = df[~invalid_req]

# -------------------------
# 4. STATUS / CHANNEL
# -------------------------
valid_status = ["abierto", "en_proceso", "cerrado", "anulado"]
valid_channel = ["web", "presencial", "callcenter", "app", "email"]

log["invalid_status"] = (~df["status"].isin(valid_status)).sum()
log["invalid_channel"] = (~df["channel"].isin(valid_channel)).sum()

df.loc[~df["status"].isin(valid_status), "status"] = np.nan
df.loc[~df["channel"].isin(valid_channel), "channel"] = "otro"

# -------------------------
# 5. CONSISTENCIA DE FECHAS
# -------------------------
df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce")

inconsistent = (df["status"] == "cerrado") & (df["closed_at"] < df["created_at"])
log["inconsistent_dates"] = inconsistent.sum()

df.loc[inconsistent, ["closed_at", "resolution_hours"]] = np.nan

df["resolution_hours_calc"] = (
    (df["closed_at"] - df["created_at"]).dt.total_seconds() / 3600
)

df["resolution_hours"] = df["resolution_hours"].fillna(df["resolution_hours_calc"])

# -------------------------
# 6. CATEGORÍA EXISTE EN OFICINAS
# -------------------------
valid_categories = oficinas["categoria_principal"].dropna().unique()

invalid_cat = ~df["category"].isin(valid_categories)
log["invalid_category"] = invalid_cat.sum()

df.loc[invalid_cat, "category"] = "OTRA"

# -------------------------
# 7. RANGOS
# -------------------------
log["invalid_rating"] = (~df["satisfaction_rating"].between(1,5)).sum()
df.loc[~df["satisfaction_rating"].between(1,5), "satisfaction_rating"] = np.nan

log["invalid_coordinates"] = (
    (~df["latitude"].between(-90,90)) |
    (~df["longitude"].between(-180,180))
).sum()

df.loc[
    (~df["latitude"].between(-90,90)) |
    (~df["longitude"].between(-180,180)),
    ["latitude","longitude"]
] = np.nan

# -------------------------
# 8. EMAIL / TELÉFONO
# -------------------------
email_regex = r"^[^@]+@[^@]+\.[^@]+$"
phone_regex = r"^\d{9}$"

log["invalid_email"] = (~df["contact_email"].astype(str).str.match(email_regex)).sum()
df.loc[~df["contact_email"].astype(str).str.match(email_regex), "contact_email"] = np.nan

log["invalid_phone"] = (~df["contact_phone"].astype(str).str.match(phone_regex)).sum()
df.loc[~df["contact_phone"].astype(str).str.match(phone_regex), "contact_phone"] = np.nan

# -------------------------
# 9. GUARDAR SILVER
# -------------------------
df = df.drop(columns=["contact_phone"], errors="ignore")
df.to_csv(SILVER_PATH, index=False)

# -------------------------
# 10. LOG DE CALIDAD
# -------------------------
log["total_read"] = total_read
log["total_valid"] = len(df)
log["total_discarded"] = total_read - len(df)
log["quality_pct"] = round((len(df)/total_read)*100,2)

log_df = pd.DataFrame([log])
log_df["run_date"] = datetime.now().strftime("%Y-%m-%d")

log_df.to_csv(LOG_PATH, index=False)

print("✅ Silver generado correctamente")
print("📄 Log de calidad:", LOG_PATH)
