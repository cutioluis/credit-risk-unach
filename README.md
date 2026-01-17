# Credit Risk Management System - UNACH

Sistema de Gestión de Clientes y Riesgo Crediticio diseñado bajo un enfoque de **Arquitectura de Software + Ciencia de Datos**, aplicando el patrón **MVC adaptado a Data Science**.

Este proyecto no es un script experimental, sino una **aplicación modular**, orientada a demostrar buenas prácticas de ingeniería de software, estructuras de datos y modelado predictivo.

---

## Objetivo del Proyecto

Desarrollar un sistema que permita:

- Analizar datos históricos de clientes financieros
- Limpiar y preparar los datos aplicando técnicas estadísticas (IQR, imputación)
- Entrenar un modelo de Machine Learning para estimar **riesgo crediticio**
- Ordenar clientes usando **estructuras de datos implementadas manualmente**
- Visualizar resultados mediante una aplicación web interactiva

---


## Conceptos Aplicados
- Arquitectura MVC
- Programación Orientada a Objetos (POO)
- Ingeniería de Datos (ETL)
- Estructuras de Datos (Heap / Cola de Prioridad)
- Machine Learning con Scikit-Learn
- Visualización de datos
- Separación de responsabilidades
- Buenas prácticas de desarrollo

---

## Arquitectura General

El sistema está dividido en **tres capas principales**:

### Data Layer (Capa de Datos)
- Ingesta de archivos CSV
- Limpieza de datos
- Eliminación de outliers
- Transformaciones y codificación

### Core Logic (Lógica de Negocio)
- Entrenamiento y predicción con Machine Learning
- Implementación de estructuras de datos (Heap)
- Cálculos matemáticos y estadísticos

### Web Layer (Presentación)
- Servidor Flask
- Vistas HTML con Jinja2
- Gráficos interactivos con Plotly


---

## Estructura del Proyecto

```plaintext
credit_risk_system/
│
├── data/
│   ├── raw/                  # Dataset original (CSV)
│   └── processed/            # Datos procesados
│
├── models/
│   ├── model_risk.pkl        # Modelo entrenado
│   └── scaler.pkl            # Escalador de datos
│
├── src/                      # Lógica de negocio (sin Flask)
│   ├── etl_pipeline.py       # Limpieza y transformación de datos
│   ├── data_structures.py    # Implementación de Heap (estructura de datos)
│   └── ml_engine.py          # Entrenamiento y predicción
│
├── static/
│   ├── css/
│   └── img/
│
├── templates/
│   ├── layout.html
│   ├── dashboard.html
│   └── predict.html
│
├── app.py                    # Controlador Flask
├── requirements.txt
└── README.md