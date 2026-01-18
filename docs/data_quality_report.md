
# Data Quality Report – Silver Layer  
**Date:** 2026-01-18  
**Source:** Bronze  
**Target:** Silver  

---

## Totals
- Total read: **522**  
- Total valid: **491**  
- Total discarded: **31**  
- Data quality: **94.06%**

---

## Nulls by Column

| Column | % Null |
|--------|--------|
| request_id | 0.0% |
| citizen_id | 2.65% |
| office_id | 0.0% |
| channel | 0.0% |
| request_type | 0.61% |
| category | 0.0% |
| subcategory | 1.02% |
| created_at | 0.0% |
| closed_at | 2.44% |
| status | 2.24% |
| priority | 0.81% |
| satisfaction_rating | 7.33% |
| resolution_hours | 1.22% |
| cost_soles | 3.26% |
| department | 1.22% |
| province | 0.61% |
| district | 1.22% |
| latitude | 9.98% |
| longitude | 9.98% |
| contact_email | 4.89% |
| resolution_hours_calc | 2.44% |

---

## Outliers by Numeric Column (P01–P99)

| Column | P01 | P99 | Outlier Count | Outlier % |
|--------|-----|-----|---------------|-----------|
| satisfaction_rating | 1.0 | 5.0 | 0 | 0.0% |
| resolution_hours | 3.84 | 800.0 | 7 | 1.43% |
| cost_soles | -50.0 | 26257.0 | 5 | 1.02% |
| latitude | -18.14 | -11.59 | 10 | 2.04% |
| longitude | -78.35 | -69.68 | 10 | 2.04% |
| resolution_hours_calc | -14.32 | 238.0 | 9 | 1.83% |

---

## Governance Decision

The column `contact_phone` was removed from the Silver layer because:

- It provides no analytical value  
- It increases privacy risk  
- It is not required for KPIs  
- It does not support decision-making  

This aligns with **data minimization** and **public-sector governance principles**.
