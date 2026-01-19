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
│   ├── raw/                       # Dataset original (CSV)
│   │   └── credit_risk_dataset.csv
│   └── processed/                 # Datos procesados
│       └── clean_data.csv
│
├── models/                        # Modelos entrenados
│   ├── credit_risk_model.pkl
│   └── scaler.pkl
│
├── src/                           # Lógica de negocio (separación de responsabilidades)
│   ├── __init__.py
│   ├── data_structures.py         # MinHeap, MaxHeap (estructuras de datos)
│   ├── data_processing.py         # ETL: Limpieza y transformación
│   ├── model.py                   # Entrenamiento y predicción ML
│   └── visualizations.py          # Gráficos con Plotly
│
├── static/
│   └── css/
│       └── style.css              # Estilos de la aplicación
│
├── templates/                     # Vistas HTML con Jinja2
│   ├── index.html
│   ├── predict.html
│   ├── results.html
│   ├── dashboard.html
│   ├── stats.html
│   └── error.html
│
├── .gitignore                     # Archivos ignorados por Git
├── config.py                      # Configuración centralizada
├── app.py                         # Aplicación Flask (punto de entrada)
├── requirements.txt               # Dependencias Python
└── README.md                      # Documentación

---

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd credit_risk_system
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv
# Activar en Windows:
venv\Scripts\activate
# Activar en Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Verificar Dataset
Asegúrate de que el archivo `data/raw/credit_risk_dataset.csv` esté presente.

---

## Uso del Sistema

### Paso 1: Procesar Datos y Entrenar Modelo

Ejecuta el siguiente script para procesar los datos y entrenar el modelo:

```python
# train_model.py (crear este archivo)
from src.data_processing import DataProcessor
from src.model import CreditRiskModel
import joblib
import config

# 1. Procesar datos
processor = DataProcessor()
X_train, X_test, y_train, y_test, df_clean = processor.process_pipeline()

# 2. Entrenar modelo
model = CreditRiskModel()
metrics = model.train_and_evaluate_pipeline(
    X_train, X_test, y_train, y_test,
    feature_names=processor.feature_names
)

# 3. Guardar scaler
joblib.dump(processor.scaler, config.SCALER_FILE)
print(f"\n✓ Scaler guardado en: {config.SCALER_FILE}")
```

```bash
python train_model.py
```

### Paso 2: Iniciar Aplicación Web

```bash
python app.py
```

Abre tu navegador en: `http://localhost:5000`

---

## Funcionalidades

### 1. Página Principal (/)
- Introducción al sistema
- Enlaces a funcionalidades principales

### 2. Predicción (/predict)
- Formulario para ingresar datos de solicitud de crédito
- Predicción de riesgo en tiempo real
- Muestra probabilidad de incumplimiento

### 3. Dashboard (/dashboard)
- Visualizaciones interactivas con Plotly:
  - Distribución de defaults
  - Histogramas por variables
  - Scatter plots
  - Box plots
  - Matriz de correlación

### 4. Estadísticas (/stats)
- Métricas generales del dataset
- Tasa de incumplimiento
- Promedios de préstamos e ingresos

---

## Estructuras de Datos Implementadas

### MinHeap
- Complejidad: O(log n) para inserción y extracción
- Uso: Encontrar las N mejores tasas de interés (más bajas)

### MaxHeap
- Complejidad: O(log n) para inserción y extracción
- Uso: Encontrar los N mayores riesgos

### Ejemplo de Uso:
```python
from src.data_structures import MinHeap, MaxHeap, get_top_n_min

# Encontrar las 5 mejores tasas de interés
tasas = [10.5, 8.2, 15.7, 6.3, 12.1, 9.8]
top_5_mejores = get_top_n_min(tasas, 5)
print(top_5_mejores)  # [6.3, 8.2, 9.8, 10.5, 12.1]
```

---

## Tecnologías Utilizadas

- **Python 3.8+**
- **Flask**: Framework web
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **Scikit-learn**: Machine Learning
- **Plotly**: Visualizaciones interactivas
- **Joblib**: Serialización de modelos

---

## Modelo de Machine Learning

- **Algoritmo**: Random Forest Classifier
- **Features**: 11 variables (edad, ingreso, monto del préstamo, etc.)
- **Target**: loan_status (0: no default, 1: default)
- **Métricas**: Accuracy, Precision, Recall, F1-Score, ROC-AUC

---

## Pipeline de Procesamiento

1. **Carga de Datos**: Lectura del CSV
2. **Limpieza**:
   - Eliminación de duplicados
   - Manejo de valores faltantes
   - Eliminación de outliers (IQR)
   - Validación de rangos
3. **Transformación**:
   - Encoding de variables categóricas
   - Normalización de features numéricas
4. **División**: Train/Test split (80/20)
5. **Entrenamiento**: Random Forest
6. **Evaluación**: Métricas de clasificación

---

## Autor

Proyecto de Programación y Estructura de Datos - UNACH