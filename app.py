"""
Aplicacion Flask para el Sistema de Prediccion de Riesgo Crediticio
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import config
from src.data_processing import DataProcessor
from src.model import CreditRiskModel
from src.visualizations import CreditRiskVisualizer
import os

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_secret_key_aqui'

# Instancias globales
processor = DataProcessor()
model = CreditRiskModel()
visualizer = CreditRiskVisualizer()

# Cargar recursos necesarios si existen
def load_model_resources():
    """Carga modelo, scaler, encoders y feature_names si existen"""
    resources = {}

    if os.path.exists(config.MODEL_FILE):
        model.load_model(config.MODEL_FILE)
        resources['model_loaded'] = True

    if os.path.exists(config.SCALER_FILE):
        resources['scaler'] = joblib.load(config.SCALER_FILE)

    if os.path.exists(config.ENCODERS_FILE):
        processor.load_encoders(config.ENCODERS_FILE)
        resources['encoders_loaded'] = True

    if os.path.exists(config.MODELS_DIR / "feature_names.pkl"):
        processor.feature_names = joblib.load(config.MODELS_DIR / "feature_names.pkl")
        resources['feature_names_loaded'] = True

    return resources

# Intentar cargar recursos al iniciar
try:
    model_resources = load_model_resources()
    print("✓ Recursos del modelo cargados exitosamente")
except Exception as e:
    print(f"⚠ Advertencia: No se pudieron cargar todos los recursos: {e}")
    print("  Ejecuta 'python train_model.py' primero para entrenar el modelo")
    model_resources = {}


@app.route('/')
def index():
    """Pagina principal"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard con visualizaciones"""
    try:
        # Cargar datos procesados
        df = pd.read_csv(config.PROCESSED_DATA_FILE)

        # Generar visualizaciones
        figures = visualizer.create_dashboard(df)

        # Convertir figuras a JSON para renderizar en HTML
        plots_json = [fig.to_json() for fig in figures]

        return render_template('dashboard.html', plots=plots_json)
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Pagina de prediccion"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            features = {
                'person_age': int(request.form['person_age']),
                'person_income': float(request.form['person_income']),
                'person_home_ownership': request.form['person_home_ownership'],
                'person_emp_length': float(request.form['person_emp_length']),
                'loan_intent': request.form['loan_intent'],
                'loan_grade': request.form['loan_grade'],
                'loan_amnt': float(request.form['loan_amnt']),
                'loan_int_rate': float(request.form['loan_int_rate']),
                'loan_percent_income': float(request.form['loan_percent_income']),
                'cb_person_default_on_file': request.form['cb_person_default_on_file'],
                'cb_person_cred_hist_length': int(request.form['cb_person_cred_hist_length'])
            }

            # Verificar que el modelo esté cargado
            if 'scaler' not in model_resources:
                raise ValueError("El modelo no ha sido entrenado. Ejecuta 'python train_model.py' primero.")

            # Realizar prediccion usando processor para transformar las features
            result = model.predict_single(features, processor, model_resources['scaler'])

            return render_template('results.html',
                                 features=features,
                                 prediction=result)
        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('predict.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint para predicciones"""
    try:
        data = request.get_json()

        # Verificar que el modelo esté cargado
        if 'scaler' not in model_resources:
            return jsonify({'error': 'El modelo no ha sido entrenado. Ejecuta train_model.py primero.'}), 503

        # Realizar prediccion usando processor para transformar las features
        result = model.predict_single(data, processor, model_resources['scaler'])

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/stats')
def stats():
    """Estad�sticas del dataset"""
    try:
        df = pd.read_csv(config.PROCESSED_DATA_FILE)

        stats = {
            'total_records': len(df),
            'default_rate': float(df['loan_status'].mean()),
            'avg_loan_amount': float(df['loan_amnt'].mean()),
            'avg_interest_rate': float(df['loan_int_rate'].mean()),
            'avg_income': float(df['person_income'].mean())
        }

        return render_template('stats.html', stats=stats)
    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
""" Agregar modelo para hacer predicciones """