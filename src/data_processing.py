"""
Módulo de procesamiento y limpieza de datos
Maneja la carga, limpieza, transformación y preparación de datos
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import config


class DataProcessor:
    """
    Clase para procesar y limpiar el dataset de riesgo crediticio
    """

    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None

    def load_data(self, filepath=None):
        """
        Carga el dataset desde un archivo CSV

        Args:
            filepath: Ruta al archivo CSV (opcional, usa config por defecto)

        Returns:
            DataFrame con los datos cargados
        """
        if filepath is None:
            filepath = config.RAW_DATA_FILE

        print(f"Cargando datos desde: {filepath}")
        df = pd.read_csv(filepath)
        print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df

    def explore_data(self, df):
        """
        Exploración inicial del dataset

        Args:
            df: DataFrame a explorar

        Returns:
            Diccionario con información del dataset
        """
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'numeric_summary': df.describe().to_dict(),
            'categorical_summary': {}
        }

        # Resumen de variables categóricas
        for col in config.CATEGORICAL_COLUMNS:
            if col in df.columns:
                info['categorical_summary'][col] = df[col].value_counts().to_dict()

        return info

    def clean_data(self, df):
        """
        Limpia el dataset: maneja valores faltantes, duplicados y outliers

        Args:
            df: DataFrame a limpiar

        Returns:
            DataFrame limpio
        """
        print("\n=== Iniciando limpieza de datos ===")
        df_clean = df.copy()
        initial_rows = len(df_clean)

        # 1. Eliminar duplicados
        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            df_clean = df_clean.drop_duplicates()
            print(f"✓ Eliminados {duplicates} registros duplicados")

        # 2. Manejar valores faltantes
        missing = df_clean.isnull().sum()
        if missing.sum() > 0:
            print("\nValores faltantes encontrados:")
            print(missing[missing > 0])

            # Estrategia: eliminar filas con valores faltantes
            # (puedes cambiar esto por imputación si prefieres)
            df_clean = df_clean.dropna()
            print(f"✓ Eliminadas {initial_rows - len(df_clean)} filas con valores faltantes")

        # 3. Eliminar outliers extremos usando IQR
        df_clean = self._remove_outliers(df_clean)

        # 4. Validar rangos de valores
        df_clean = self._validate_ranges(df_clean)

        print(f"\n✓ Limpieza completada: {len(df_clean)} registros finales")
        print(f"  (reducción de {initial_rows - len(df_clean)} registros)")

        return df_clean

    def _remove_outliers(self, df):
        """
        Elimina outliers extremos usando el método IQR

        Args:
            df: DataFrame

        Returns:
            DataFrame sin outliers extremos
        """
        df_no_outliers = df.copy()
        initial_rows = len(df_no_outliers)

        for col in config.NUMERICAL_COLUMNS:
            if col in df_no_outliers.columns:
                Q1 = df_no_outliers[col].quantile(0.25)
                Q3 = df_no_outliers[col].quantile(0.75)
                IQR = Q3 - Q1

                # Límites: Q1 - 3*IQR y Q3 + 3*IQR (más permisivo que 1.5*IQR)
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR

                # Filtrar outliers extremos
                outliers = ((df_no_outliers[col] < lower_bound) |
                           (df_no_outliers[col] > upper_bound)).sum()

                if outliers > 0:
                    df_no_outliers = df_no_outliers[
                        (df_no_outliers[col] >= lower_bound) &
                        (df_no_outliers[col] <= upper_bound)
                    ]

        removed = initial_rows - len(df_no_outliers)
        if removed > 0:
            print(f"✓ Eliminados {removed} outliers extremos")

        return df_no_outliers

    def _validate_ranges(self, df):
        """
        Valida que los valores estén en rangos lógicos

        Args:
            df: DataFrame

        Returns:
            DataFrame validado
        """
        df_valid = df.copy()
        initial_rows = len(df_valid)

        # Edad: entre 18 y 100 años
        if 'person_age' in df_valid.columns:
            df_valid = df_valid[(df_valid['person_age'] >= 18) &
                               (df_valid['person_age'] <= 100)]

        # Ingreso: mayor a 0
        if 'person_income' in df_valid.columns:
            df_valid = df_valid[df_valid['person_income'] > 0]

        # Años de empleo: no negativo
        if 'person_emp_length' in df_valid.columns:
            df_valid = df_valid[df_valid['person_emp_length'] >= 0]

        # Monto del préstamo: mayor a 0
        if 'loan_amnt' in df_valid.columns:
            df_valid = df_valid[df_valid['loan_amnt'] > 0]

        # Tasa de interés: entre 0 y 100%
        if 'loan_int_rate' in df_valid.columns:
            df_valid = df_valid[(df_valid['loan_int_rate'] >= 0) &
                               (df_valid['loan_int_rate'] <= 100)]

        removed = initial_rows - len(df_valid)
        if removed > 0:
            print(f"✓ Eliminados {removed} registros con valores fuera de rango")

        return df_valid

    def encode_categorical(self, df):
        """
        Codifica variables categóricas usando Label Encoding

        Args:
            df: DataFrame con variables categóricas

        Returns:
            DataFrame con variables codificadas
        """
        df_encoded = df.copy()

        print("\n=== Codificando variables categóricas ===")
        for col in config.CATEGORICAL_COLUMNS:
            if col in df_encoded.columns:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col])
                self.label_encoders[col] = le
                print(f"✓ {col}: {len(le.classes_)} categorías")

        return df_encoded

    def prepare_features(self, df, scale=True):
        """
        Prepara las features para el modelo: separa X e y, escala features

        Args:
            df: DataFrame procesado
            scale: Si se debe escalar las features numéricas

        Returns:
            X_train, X_test, y_train, y_test
        """
        print("\n=== Preparando features para el modelo ===")

        # Separar features y target
        X = df.drop(columns=[config.TARGET_COLUMN])
        y = df[config.TARGET_COLUMN]

        # Guardar nombres de features
        self.feature_names = X.columns.tolist()

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=config.TEST_SIZE,
            random_state=config.RANDOM_STATE,
            stratify=y
        )

        print(f"✓ Train set: {X_train.shape[0]} muestras")
        print(f"✓ Test set: {X_test.shape[0]} muestras")
        print(f"✓ Distribución de clases en train: {y_train.value_counts().to_dict()}")

        # Escalar features numéricas
        if scale:
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            print("✓ Features escaladas con StandardScaler")

        return X_train, X_test, y_train, y_test

    def save_processed_data(self, df, filepath=None):
        """
        Guarda el dataset procesado

        Args:
            df: DataFrame procesado
            filepath: Ruta donde guardar (opcional, usa config por defecto)
        """
        if filepath is None:
            filepath = config.PROCESSED_DATA_FILE

        df.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados en: {filepath}")

    def process_pipeline(self):
        """
        Pipeline completo de procesamiento de datos

        Returns:
            X_train, X_test, y_train, y_test, df_clean
        """
        print("\n" + "="*60)
        print("PIPELINE DE PROCESAMIENTO DE DATOS")
        print("="*60)

        # 1. Cargar datos
        df = self.load_data()

        # 2. Explorar datos
        info = self.explore_data(df)
        print(f"\nDataset inicial: {info['shape']}")

        # 3. Limpiar datos
        df_clean = self.clean_data(df)

        # 4. Codificar categóricas
        df_encoded = self.encode_categorical(df_clean)

        # 5. Guardar datos procesados
        self.save_processed_data(df_encoded)

        # 6. Preparar features
        X_train, X_test, y_train, y_test = self.prepare_features(df_encoded)

        print("\n" + "="*60)
        print("✓ PIPELINE COMPLETADO EXITOSAMENTE")
        print("="*60 + "\n")

        return X_train, X_test, y_train, y_test, df_clean

    def save_encoders(self, filepath=None):
        """
        Guarda los label encoders entrenados

        Args:
            filepath: Ruta donde guardar los encoders (opcional, usa config por defecto)
        """
        if filepath is None:
            filepath = config.ENCODERS_FILE

        joblib.dump(self.label_encoders, filepath)
        print(f"✓ Label encoders guardados en: {filepath}")

    def load_encoders(self, filepath=None):
        """
        Carga los label encoders previamente guardados

        Args:
            filepath: Ruta de los encoders a cargar (opcional, usa config por defecto)
        """
        if filepath is None:
            filepath = config.ENCODERS_FILE

        self.label_encoders = joblib.load(filepath)
        print(f"✓ Label encoders cargados desde: {filepath}")

    def transform_single_input(self, features_dict):
        """
        Transforma un diccionario de features para predicción
        Codifica variables categóricas y ordena las features correctamente

        Args:
            features_dict: Diccionario con las features (puede contener valores categóricos como strings)

        Returns:
            DataFrame con las features transformadas y ordenadas
        """
        # Crear DataFrame desde el diccionario
        df = pd.DataFrame([features_dict])

        # Codificar variables categóricas
        for col in config.CATEGORICAL_COLUMNS:
            if col in df.columns and col in self.label_encoders:
                le = self.label_encoders[col]
                try:
                    df[col] = le.transform(df[col])
                except ValueError as e:
                    # Si el valor no existe en el encoder, usar el más común (0)
                    print(f"⚠ Advertencia: Valor '{df[col].iloc[0]}' no reconocido en {col}, usando valor por defecto")
                    df[col] = 0

        # Ordenar columnas en el orden correcto (mismo orden que en entrenamiento)
        if self.feature_names is not None:
            df = df[self.feature_names]

        return df
