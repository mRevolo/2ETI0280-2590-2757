# 📄 Instrucciones de Evaluación Final

## 📊 Proyecto: Arquitectura Medallón - Servicio Ciudadano

Este repositorio contiene la implementación de un flujo de datos (ETL) profesional utilizando la metodología **Medallion Architecture**. El objetivo es procesar solicitudes ciudadanas desde su estado crudo hasta la generación de KPIs de negocio listos para la toma de decisiones.

---

## 🛠️ 1. Requisitos Previos

Para ejecutar este proyecto, es necesario tener instalado **Python 3.x** y las siguientes librerías:

* **Pandas**: Para la manipulación y limpieza de datos.
* **Numpy**: Para operaciones lógicas y manejo de valores nulos.

### Instalación rápida
Abre una terminal en la carpeta raíz del proyecto y ejecuta:
bash
pip install pandas numpy


## 📂 2. Estructura del Repositorio
El proyecto sigue una estructura de directorios estricta para garantizar la reproducibilidad:

data/bronze/: Datasets originales (oficinas.csv y solicitudes_ciudadanas.csv).

data/silver/: Datos limpios y normalizados (generados por el pipeline).

data/gold/: KPIs agregados por oficina y periodo (generados por el pipeline).

pipelines/: Scripts de Python que contienen la lógica de transformación.

docs/: Reportes de calidad (DQ), diccionarios de datos y reglas de gobierno.

## 🚀 3. Pasos para la Ejecución
Para que el proyecto funcione correctamente, los scripts deben ejecutarse en el siguiente orden desde la carpeta raíz:

Paso 1: Procesamiento de Capa Silver
Este script limpia los datos crudos, valida formatos de email, normaliza fechas y elimina registros incompletos.

Bash

python pipelines/bronce_to_silver.py
Paso 2: Ejecución del Reporte de Calidad (DQ)
Genera el informe técnico de salud de los datos (nulos, duplicados y outliers).

Bash

python pipelines/DATA_QUALITY_REPORT.py
Paso 3: Generación de Capa Gold (KPIs)
Calcula las métricas de negocio (Satisfacción promedio, % de digitalización, tiempos de respuesta).

Bash

python pipelines/silver_to_gold.py
## 📋 4. Rúbrica Técnica Cubierta
Reglas de Limpieza: Justificadas detalladamente en docs/reglas_silver_calidad_datos.md.

Data Quality (DQ): Reporte automatizado disponible en docs/data_quality_report.md.

Arquitectura Medallón: Separación física de datos en Bronze, Silver y Gold.

KPIs y Linaje: Definiciones de negocio y dueños de datos en docs/gobierno_datos_kpis_servicio_ciudadano.md.

Portabilidad: Uso de la librería pathlib para garantizar que las rutas funcionen en Windows, Mac y Linux sin modificaciones.

