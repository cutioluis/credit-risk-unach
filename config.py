"""
Configuración centralizada del sistema de Credit Risk Prediction
"""
import os
from pathlib import Path

# Directorios base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Archivos de datos
RAW_DATA_FILE = RAW_DATA_DIR / "credit_risk_dataset.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "clean_data.csv"

# Archivos de modelos
MODEL_FILE = MODELS_DIR / "credit_risk_model.pkl"
SCALER_FILE = MODELS_DIR / "scaler.pkl"
ENCODERS_FILE = MODELS_DIR / "label_encoders.pkl"

# Configuración del modelo
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'random_state': RANDOM_STATE
}

# Columnas del dataset
TARGET_COLUMN = 'loan_status'
CATEGORICAL_COLUMNS = [
    'person_home_ownership',
    'loan_intent',
    'loan_grade',
    'cb_person_default_on_file'
]
NUMERICAL_COLUMNS = [
    'person_age',
    'person_income',
    'person_emp_length',
    'loan_amnt',
    'loan_int_rate',
    'loan_percent_income',
    'cb_person_cred_hist_length'
]

# Configuración Flask
DEBUG = os.getenv('DEBUG', 'True') == 'True'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Configuración de visualizaciones
PLOTLY_TEMPLATE = 'plotly_white'
PLOT_HEIGHT = 500
PLOT_WIDTH = 800
