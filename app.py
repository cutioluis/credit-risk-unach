"""
Aplicacion Flask para el Sistema de Prediccion de Riesgo Crediticio
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import json
import config
from src.data_processing import DataProcessor
from src.model import CreditRiskModel
from src.visualizations import CreditRiskVisualizer
from src.data_structures import CreditRiskBST
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
    """Estadisticas del dataset"""
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


@app.route('/arbol')
def arbol():
    """Pagina de demostracion del Arbol Binario de Busqueda"""
    try:
        # Intentar cargar datos procesados, si no existen usar datos raw
        if os.path.exists(config.PROCESSED_DATA_FILE):
            df = pd.read_csv(config.PROCESSED_DATA_FILE)
        elif os.path.exists(config.RAW_DATA_FILE):
            df = pd.read_csv(config.RAW_DATA_FILE)
            # Limpiar datos basicos (eliminar nulos)
            df = df.dropna()
        else:
            raise FileNotFoundError("No se encontraron archivos de datos")

        # Crear scores de riesgo simulados basados en loan_status y otras features
        # Score de riesgo: 0-100 (mayor = mas riesgo)
        np.random.seed(42)

        # Calcular score basado en features relevantes
        risk_scores = []
        for idx, row in df.iterrows():
            base_score = row['loan_status'] * 50  # 0 o 50 segun default
            # Ajustar por tasa de interes (normalizada)
            interest_factor = min(row['loan_int_rate'] / 25 * 30, 30)
            # Ajustar por porcentaje de ingreso
            income_factor = min(row['loan_percent_income'] * 50, 20)
            # Agregar variacion aleatoria
            noise = np.random.uniform(-5, 5)

            score = base_score + interest_factor + income_factor + noise
            score = max(0, min(100, score))  # Limitar entre 0 y 100
            risk_scores.append(int(score))

        # Construir el BST con una muestra de datos (para visualizacion)
        sample_size = min(50, len(df))
        sample_indices = np.random.choice(len(df), sample_size, replace=False)

        bst = CreditRiskBST()
        for idx in sample_indices:
            score = risk_scores[idx]
            client_data = {
                'index': int(idx),
                'loan_amnt': float(df.iloc[idx]['loan_amnt']),
                'income': float(df.iloc[idx]['person_income'])
            }
            bst.insert_client(score, client_data)

        # Obtener parametros de busqueda en rango
        range_min = request.args.get('min_score', 0, type=int)
        range_max = request.args.get('max_score', 100, type=int)

        # Busqueda en rango
        range_results = bst.range_search(range_min, range_max)

        # Estadisticas del arbol
        tree_stats = {
            'total_nodes': bst.size(),
            'height': bst.height(),
            'min_risk': bst.find_min().key if not bst.is_empty() else 0,
            'max_risk': bst.find_max().key if not bst.is_empty() else 0
        }

        # Recorridos
        traversals = {
            'inorder': bst.inorder(),
            'preorder': bst.preorder(),
            'postorder': bst.postorder(),
            'levelorder': bst.level_order()
        }

        # Distribucion de riesgo
        distribution = bst.get_risk_distribution()

        # Convertir arbol a JSON para D3.js
        def tree_to_dict(node):
            if node is None:
                return None
            result = {
                'key': node.key,
                'data': node.data
            }
            children = []
            if node.left:
                children.append(tree_to_dict(node.left))
            if node.right:
                children.append(tree_to_dict(node.right))
            if children:
                result['children'] = children
            return result

        tree_json = json.dumps(tree_to_dict(bst.root))

        return render_template('arbol.html',
                               tree_data=True,
                               tree_json=tree_json,
                               stats=tree_stats,
                               traversals=traversals,
                               distribution=distribution,
                               range_results=range_results,
                               range_min=range_min,
                               range_max=range_max)

    except Exception as e:
        return render_template('arbol.html', tree_data=False, error=str(e))


if __name__ == '__main__':
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
""" Agregar modelo para hacer predicciones """