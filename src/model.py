"""
Módulo de Machine Learning
Maneja el entrenamiento, evaluación y predicción del modelo
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)
import joblib
import config


class CreditRiskModel:
    """
    Clase para entrenar y usar el modelo de predicción de riesgo crediticio
    """

    def __init__(self):
        self.model = None
        self.metrics = {}
        self.feature_importance = None

    def train(self, X_train, y_train):
        """
        Entrena el modelo de Random Forest

        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento

        Returns:
            Modelo entrenado
        """
        print("\n=== Entrenando modelo Random Forest ===")
        print(f"Parámetros: {config.MODEL_PARAMS}")

        self.model = RandomForestClassifier(**config.MODEL_PARAMS)
        self.model.fit(X_train, y_train)

        print("✓ Modelo entrenado exitosamente")
        return self.model

    def evaluate(self, X_test, y_test):
        """
        Evalúa el modelo en el conjunto de prueba

        Args:
            X_test: Features de prueba
            y_test: Target de prueba

        Returns:
            Diccionario con las métricas de evaluación
        """
        if self.model is None:
            raise ValueError("El modelo no ha sido entrenado")

        print("\n=== Evaluando modelo ===")

        # Predicciones
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        # Calcular métricas
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred)
        }

        # Mostrar métricas
        print("\n📊 Métricas de Evaluación:")
        print(f"  • Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"  • Precision: {self.metrics['precision']:.4f}")
        print(f"  • Recall:    {self.metrics['recall']:.4f}")
        print(f"  • F1-Score:  {self.metrics['f1_score']:.4f}")
        print(f"  • ROC-AUC:   {self.metrics['roc_auc']:.4f}")

        print("\n📋 Matriz de Confusión:")
        cm = self.metrics['confusion_matrix']
        print(f"  TN: {cm[0][0]:<6} FP: {cm[0][1]:<6}")
        print(f"  FN: {cm[1][0]:<6} TP: {cm[1][1]:<6}")

        return self.metrics

    def get_feature_importance(self, feature_names):
        """
        Obtiene la importancia de las features

        Args:
            feature_names: Lista con nombres de las features

        Returns:
            DataFrame con las importancias ordenadas
        """
        if self.model is None:
            raise ValueError("El modelo no ha sido entrenado")

        importances = self.model.feature_importances_
        self.feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)

        print("\n📈 Top 5 Features más importantes:")
        for idx, row in self.feature_importance.head().iterrows():
            print(f"  {row['feature']:<30} {row['importance']:.4f}")

        return self.feature_importance

    def predict(self, X):
        """
        Realiza predicciones con el modelo entrenado

        Args:
            X: Features para predecir

        Returns:
            Predicciones (0: no default, 1: default)
        """
        if self.model is None:
            raise ValueError("El modelo no ha sido entrenado")

        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Obtiene probabilidades de predicción

        Args:
            X: Features para predecir

        Returns:
            Array con probabilidades [prob_no_default, prob_default]
        """
        if self.model is None:
            raise ValueError("El modelo no ha sido entrenado")

        return self.model.predict_proba(X)

    def predict_single(self, features_dict, processor, scaler):
        """
        Predice para una única solicitud de crédito

        Args:
            features_dict: Diccionario con las features (puede contener valores categóricos como strings)
            processor: Instancia de DataProcessor para transformar las features
            scaler: Scaler para normalizar las features

        Returns:
            Diccionario con la predicción y probabilidades
        """
        # Transformar el input usando el processor (codifica categóricas y ordena features)
        df_transformed = processor.transform_single_input(features_dict)

        # Escalar las features
        X = scaler.transform(df_transformed)

        # Predecir
        prediction = self.predict(X)[0]
        proba = self.predict_proba(X)[0]

        risk_level = "ALTO RIESGO" if prediction == 1 else "BAJO RIESGO"
        confidence = proba[1] if prediction == 1 else proba[0]

        return {
            'prediction': int(prediction),
            'risk_level': risk_level,
            'probability_default': float(proba[1]),
            'probability_no_default': float(proba[0]),
            'confidence': float(confidence)
        }

    def save_model(self, filepath=None):
        """
        Guarda el modelo entrenado

        Args:
            filepath: Ruta donde guardar el modelo
        """
        if filepath is None:
            filepath = config.MODEL_FILE

        joblib.dump(self.model, filepath)
        print(f"\n✓ Modelo guardado en: {filepath}")

    def load_model(self, filepath=None):
        """
        Carga un modelo previamente entrenado

        Args:
            filepath: Ruta del modelo a cargar
        """
        if filepath is None:
            filepath = config.MODEL_FILE

        self.model = joblib.load(filepath)
        print(f"✓ Modelo cargado desde: {filepath}")

    def train_and_evaluate_pipeline(self, X_train, X_test, y_train, y_test, feature_names):
        """
        Pipeline completo de entrenamiento y evaluación

        Args:
            X_train: Features de entrenamiento
            X_test: Features de prueba
            y_train: Target de entrenamiento
            y_test: Target de prueba
            feature_names: Nombres de las features

        Returns:
            Diccionario con métricas
        """
        print("\n" + "="*60)
        print("PIPELINE DE ENTRENAMIENTO DEL MODELO")
        print("="*60)

        # 1. Entrenar
        self.train(X_train, y_train)

        # 2. Evaluar
        metrics = self.evaluate(X_test, y_test)

        # 3. Feature importance
        self.get_feature_importance(feature_names)

        # 4. Guardar modelo
        self.save_model()

        print("\n" + "="*60)
        print("✓ PIPELINE DE ENTRENAMIENTO COMPLETADO")
        print("="*60 + "\n")

        return metrics


def calculate_risk_metrics(df):
    """
    Calcula métricas de riesgo del dataset

    Args:
        df: DataFrame con los datos

    Returns:
        Diccionario con métricas de riesgo
    """
    metrics = {
        'total_loans': len(df),
        'default_rate': df['loan_status'].mean(),
        'avg_loan_amount': df['loan_amnt'].mean(),
        'avg_interest_rate': df['loan_int_rate'].mean(),
        'avg_income': df['person_income'].mean(),
    }

    # Métricas por categoría
    if 'loan_grade' in df.columns:
        metrics['default_by_grade'] = df.groupby('loan_grade')['loan_status'].mean().to_dict()

    if 'loan_intent' in df.columns:
        metrics['default_by_intent'] = df.groupby('loan_intent')['loan_status'].mean().to_dict()

    return metrics
