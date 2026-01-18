
# Reglas de Calidad de Datos – Capa Silver
Proyecto: Servicio Ciudadano
Arquitectura: Medallion (Bronze → Silver → Gold)

## 1. Completitud
Campos obligatorios:
- request_id
- office_id
- created_at
- status
- category

Registros con valores nulos en estos campos son eliminados.

## 2. Unicidad
request_id debe ser único.
Duplicados: se conserva el más reciente (created_at).

## 3. Validez

### request_id
Formato: REQ-####

### status
Valores permitidos: abierto, en_proceso, cerrado, anulado

### channel
Valores permitidos: web, presencial, callcenter, app, email

### satisfaction_rating
Rango: 1 a 5

### Coordenadas
latitude: [-90,90]
longitude: [-180,180]

## 4. Consistencia
Si status = cerrado y closed_at < created_at:
- closed_at = NULL
- resolution_hours = NULL

resolution_hours se recalcula con fechas válidas.

## 5. Catálogo
category debe existir en oficinas.csv (categoria_principal).
Si no, se asigna "OTRA".

## 6. Formato

### Email
Formato válido: usuario@dominio.com

### Teléfono
9 dígitos exactos (luego eliminado por minimización).

## 7. Minimización
Se elimina contact_phone.

## 8. Log de calidad
Se registran:
- total_read
- total_valid
- total_discarded
- quality_pct
- errores por regla

Archivo: data/silver/data_quality_log.csv
