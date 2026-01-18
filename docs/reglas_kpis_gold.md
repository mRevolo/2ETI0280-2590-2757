
# Reglas de KPIs – Capa Gold
Proyecto: Servicio Ciudadano
Fuente: Capa Silver

## 1. Grano
office_id + period_year + period_month

## 2. Periodo
Derivado de created_at:
- period_year
- period_month
- period_start

## 3. Clasificación
is_closed = status == cerrado
is_cancelled = status == anulado
is_digital = channel in {web, app, email}

## 4. KPIs

total_requests = COUNT(request_id)
closed_requests = SUM(is_closed)
cancelled_requests = SUM(is_cancelled)
digital_requests = SUM(is_digital)

avg_resolution_hours = AVG(resolution_hours)
avg_cost_soles = AVG(cost_soles)
avg_satisfaction = AVG(satisfaction_rating)

## 5. Porcentajes
pct_closed = closed_requests / total_requests * 100
pct_cancelled = cancelled_requests / total_requests * 100
pct_digital = digital_requests / total_requests * 100

## 6. Categoría principal
top_category = categoría más frecuente
category_count = número de solicitudes

## 7. Redondeo
Métricas redondeadas a 2 decimales.

## 8. Salida
Archivo: data/gold/kpis_servicio_ciudadano.csv
