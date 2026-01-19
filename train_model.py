"""
Script para entrenar el modelo de Credit Risk Prediction
Ejecuta el pipeline completo de procesamiento y entrenamiento
"""
from src.data_processing import DataProcessor
from src.model import CreditRiskModel
import joblib
import config


def main():
    """
    Pipeline completo de entrenamiento
    """
    print("="*70)
    print("CREDIT RISK PREDICTION SYSTEM - ENTRENAMIENTO")
    print("="*70)

    # 1. Procesar datos
    print("\n[1/3] Procesando datos...")
    processor = DataProcessor()
    X_train, X_test, y_train, y_test, df_clean = processor.process_pipeline()

    # 2. Entrenar modelo
    print("\n[2/3] Entrenando modelo...")
    model = CreditRiskModel()
    metrics = model.train_and_evaluate_pipeline(
        X_train, X_test, y_train, y_test,
        feature_names=processor.feature_names
    )

    # 3. Guardar scaler y encoders
    print("\n[3/3] Guardando scaler y encoders...")
    joblib.dump(processor.scaler, config.SCALER_FILE)
    print(f"✓ Scaler guardado en: {config.SCALER_FILE}")

    processor.save_encoders()

    # También guardar feature_names para referencia
    joblib.dump(processor.feature_names, config.MODELS_DIR / "feature_names.pkl")
    print(f"✓ Feature names guardados en: {config.MODELS_DIR / 'feature_names.pkl'}")

    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DEL ENTRENAMIENTO")
    print("="*70)
    print(f"Datos de entrenamiento: {len(X_train)} muestras")
    print(f"Datos de prueba: {len(X_test)} muestras")
    print(f"\nMétricas del Modelo:")
    print(f"  • Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  • Precision: {metrics['precision']:.4f}")
    print(f"  • Recall:    {metrics['recall']:.4f}")
    print(f"  • F1-Score:  {metrics['f1_score']:.4f}")
    print(f"  • ROC-AUC:   {metrics['roc_auc']:.4f}")
    print("\n" + "="*70)
    print("✓ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("="*70)
    print("\nAhora puedes ejecutar la aplicación web con: python app.py")


if __name__ == "__main__":
    main()
