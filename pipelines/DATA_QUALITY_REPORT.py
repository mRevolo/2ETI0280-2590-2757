## DATA QUALITY REPORT
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# 1. Configurar rutas relativas
BASE_DIR = Path(__file__).resolve().parent.parent
SILVER_PATH = BASE_DIR / "data" / "silver" / "solicitudes_clean.csv"
BRONZE_PATH = BASE_DIR / "data" / "bronze" / "solicitudes_ciudadanas.csv"
DOCS_PATH = BASE_DIR / "docs" / "data_quality_report.md"

silver = pd.read_csv(SILVER_PATH)
bronze = pd.read_csv(BRONZE_PATH)

#silver = pd.read_csv("/content/data/silver/solicitudes_clean.csv")
#bronze = pd.read_csv("/content/data/bronze/solicitudes_ciudadanas.csv")

# Metrics
total_read = len(bronze)
total_valid = len(silver)
total_discarded = total_read - total_valid
quality_pct = round((total_valid / total_read) * 100, 2)

# Remove contact_phone if still present
silver = silver.drop(columns=["contact_phone"], errors="ignore")

# Nulls
nulls = (silver.isnull().mean() * 100).round(2)

# Numeric columns
numeric_cols = silver.select_dtypes(include=[np.number]).columns

# Outliers (P01–P99)
outlier_summary = []

for col in numeric_cols:
    p01 = silver[col].quantile(0.01)
    p99 = silver[col].quantile(0.99)
    
    outliers = silver[(silver[col] < p01) | (silver[col] > p99)]
    
    outlier_summary.append({
        "column": col,
        "p01": round(p01, 2),
        "p99": round(p99, 2),
        "outlier_count": len(outliers),
        "outlier_pct": round((len(outliers) / len(silver)) * 100, 2)
    })

outliers_df = pd.DataFrame(outlier_summary)

# Markdown
md = f"""
# Data Quality Report – Silver Layer  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Source:** Bronze  
**Target:** Silver  

---

## Totals
- Total read: **{total_read}**  
- Total valid: **{total_valid}**  
- Total discarded: **{total_discarded}**  
- Data quality: **{quality_pct}%**

---

## Nulls by Column

| Column | % Null |
|--------|--------|
"""

for col, val in nulls.items():
    md += f"| {col} | {val}% |\n"

md += """
---

## Outliers by Numeric Column (P01–P99)

| Column | P01 | P99 | Outlier Count | Outlier % |
|--------|-----|-----|---------------|-----------|
"""

for _, row in outliers_df.iterrows():
    md += f"| {row['column']} | {row['p01']} | {row['p99']} | {row['outlier_count']} | {row['outlier_pct']}% |\n"

md += """
---

## Governance Decision by implementer

The column `contact_phone` was removed from the Silver layer because:

- It provides no analytical value  
- It increases privacy risk  
- It is not required for KPIs  
- It does not support decision-making  

This aligns with **data minimization** and **public-sector governance principles**.
"""

# Save report coolab
#file_path = "/content/data_quality_report.md"
#with open(file_path, "w", encoding="utf-8") as f:
#    f.write(md)

#file_path


REPORT_PATH = BASE_DIR / "docs" / "data_quality_report.md"

# Guardar el contenido del reporte (la variable 'md') en el archivo
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(md)

print(f"✅ Reporte de calidad guardado exitosamente en: {REPORT_PATH}")