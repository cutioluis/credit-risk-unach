"""
Módulo de visualizaciones
Genera gráficos interactivos con Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import config


class CreditRiskVisualizer:
    """
    Clase para generar visualizaciones del análisis de riesgo crediticio
    """

    def __init__(self):
        self.template = config.PLOTLY_TEMPLATE
        self.height = config.PLOT_HEIGHT
        self.width = config.PLOT_WIDTH

    def plot_histogram(self, df, column, title=None, color='steelblue', nbins=30):
        """
        Crea un histograma interactivo

        Args:
            df: DataFrame con los datos
            column: Columna a graficar
            title: Título del gráfico
            color: Color de las barras
            nbins: Número de bins

        Returns:
            Objeto figura de Plotly
        """
        if title is None:
            title = f"Distribución de {column}"

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=df[column],
            nbinsx=nbins,
            marker_color=color,
            name=column,
            opacity=0.75
        ))

        fig.update_layout(
            title=title,
            xaxis_title=column,
            yaxis_title="Frecuencia",
            template=self.template,
            height=self.height,
            width=self.width,
            showlegend=False
        )

        return fig

    def plot_histogram_by_target(self, df, column, target_col='loan_status'):
        """
        Crea histogramas superpuestos por clase objetivo

        Args:
            df: DataFrame con los datos
            column: Columna a graficar
            target_col: Columna objetivo

        Returns:
            Objeto figura de Plotly
        """
        fig = go.Figure()

        # Histograma para clase 0 (no default)
        fig.add_trace(go.Histogram(
            x=df[df[target_col] == 0][column],
            name='No Default',
            marker_color='green',
            opacity=0.6,
            nbinsx=30
        ))

        # Histograma para clase 1 (default)
        fig.add_trace(go.Histogram(
            x=df[df[target_col] == 1][column],
            name='Default',
            marker_color='red',
            opacity=0.6,
            nbinsx=30
        ))

        fig.update_layout(
            title=f"Distribución de {column} por Estado de Préstamo",
            xaxis_title=column,
            yaxis_title="Frecuencia",
            template=self.template,
            height=self.height,
            width=self.width,
            barmode='overlay'
        )

        return fig

    def plot_scatter(self, df, x_col, y_col, color_col=None, title=None):
        """
        Crea un scatter plot interactivo

        Args:
            df: DataFrame con los datos
            x_col: Columna para eje X
            y_col: Columna para eje Y
            color_col: Columna para colorear puntos
            title: Título del gráfico

        Returns:
            Objeto figura de Plotly
        """
        if title is None:
            title = f"{y_col} vs {x_col}"

        if color_col:
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                template=self.template,
                height=self.height,
                width=self.width,
                color_discrete_map={0: 'green', 1: 'red'},
                labels={0: 'No Default', 1: 'Default'}
            )
        else:
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=title,
                template=self.template,
                height=self.height,
                width=self.width
            )

        fig.update_traces(marker=dict(size=5, opacity=0.6))

        return fig

    def plot_boxplot(self, df, column, by_column=None, title=None):
        """
        Crea un box plot interactivo

        Args:
            df: DataFrame con los datos
            column: Columna a graficar
            by_column: Columna para agrupar
            title: Título del gráfico

        Returns:
            Objeto figura de Plotly
        """
        if title is None:
            if by_column:
                title = f"Box Plot de {column} por {by_column}"
            else:
                title = f"Box Plot de {column}"

        if by_column:
            fig = px.box(
                df,
                x=by_column,
                y=column,
                title=title,
                template=self.template,
                height=self.height,
                width=self.width,
                color=by_column
            )
        else:
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=df[column],
                name=column,
                marker_color='steelblue'
            ))

            fig.update_layout(
                title=title,
                yaxis_title=column,
                template=self.template,
                height=self.height,
                width=self.width
            )

        return fig

    def plot_correlation_heatmap(self, df):
        """
        Crea un mapa de calor de correlaciones

        Args:
            df: DataFrame con los datos

        Returns:
            Objeto figura de Plotly
        """
        # Calcular correlaciones
        corr = df.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlación")
        ))

        fig.update_layout(
            title="Matriz de Correlación",
            template=self.template,
            height=700,
            width=800
        )

        return fig

    def plot_feature_importance(self, feature_importance_df, top_n=10):
        """
        Gráfico de barras de importancia de features

        Args:
            feature_importance_df: DataFrame con columnas 'feature' e 'importance'
            top_n: Número de features top a mostrar

        Returns:
            Objeto figura de Plotly
        """
        top_features = feature_importance_df.head(top_n)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=top_features['importance'],
            y=top_features['feature'],
            orientation='h',
            marker_color='steelblue'
        ))

        fig.update_layout(
            title=f"Top {top_n} Features más Importantes",
            xaxis_title="Importancia",
            yaxis_title="Feature",
            template=self.template,
            height=self.height,
            width=self.width,
            yaxis={'categoryorder': 'total ascending'}
        )

        return fig

    def plot_confusion_matrix(self, cm):
        """
        Visualiza la matriz de confusión

        Args:
            cm: Matriz de confusión (2x2 array)

        Returns:
            Objeto figura de Plotly
        """
        labels = ['No Default', 'Default']

        # Crear texto para cada celda
        text = [[f'TN<br>{cm[0][0]}', f'FP<br>{cm[0][1]}'],
                [f'FN<br>{cm[1][0]}', f'TP<br>{cm[1][1]}']]

        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale='Blues',
            text=text,
            texttemplate='%{text}',
            textfont={"size": 16},
            showscale=True
        ))

        fig.update_layout(
            title="Matriz de Confusión",
            xaxis_title="Predicción",
            yaxis_title="Real",
            template=self.template,
            height=500,
            width=600
        )

        return fig

    def plot_default_distribution(self, df, target_col='loan_status'):
        """
        Gráfico de pie chart de distribución de defaults

        Args:
            df: DataFrame con los datos
            target_col: Columna objetivo

        Returns:
            Objeto figura de Plotly
        """
        counts = df[target_col].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=['No Default', 'Default'],
            values=counts.values,
            marker_colors=['green', 'red'],
            hole=0.3
        )])

        fig.update_layout(
            title="Distribución de Estados de Préstamo",
            template=self.template,
            height=self.height,
            width=self.width
        )

        return fig

    def plot_categorical_distribution(self, df, column, target_col='loan_status'):
        """
        Gráfico de barras agrupadas para variables categóricas

        Args:
            df: DataFrame con los datos
            column: Columna categórica
            target_col: Columna objetivo

        Returns:
            Objeto figura de Plotly
        """
        # Agrupar y contar
        grouped = df.groupby([column, target_col]).size().unstack(fill_value=0)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='No Default',
            x=grouped.index,
            y=grouped[0] if 0 in grouped.columns else [],
            marker_color='green'
        ))

        fig.add_trace(go.Bar(
            name='Default',
            x=grouped.index,
            y=grouped[1] if 1 in grouped.columns else [],
            marker_color='red'
        ))

        fig.update_layout(
            title=f"Distribución de {column} por Estado de Préstamo",
            xaxis_title=column,
            yaxis_title="Cantidad",
            template=self.template,
            height=self.height,
            width=self.width,
            barmode='group'
        )

        return fig

    def create_dashboard(self, df, metrics=None):
        """
        Crea un dashboard con múltiples visualizaciones

        Args:
            df: DataFrame con los datos
            metrics: Diccionario con métricas del modelo (opcional)

        Returns:
            Lista de figuras de Plotly
        """
        figures = []

        # 1. Distribución de defaults
        figures.append(self.plot_default_distribution(df))

        # 2. Histogramas de variables numéricas importantes
        numeric_cols = ['person_age', 'person_income', 'loan_amnt', 'loan_int_rate']
        for col in numeric_cols:
            if col in df.columns:
                figures.append(self.plot_histogram_by_target(df, col))

        # 3. Scatter plots
        figures.append(self.plot_scatter(
            df, 'person_income', 'loan_amnt', 'loan_status',
            title="Monto del Préstamo vs Ingreso"
        ))

        # 4. Box plots
        figures.append(self.plot_boxplot(
            df, 'loan_int_rate', 'loan_status',
            title="Tasa de Interés por Estado de Préstamo"
        ))

        # 5. Matriz de confusión (si hay métricas)
        if metrics and 'confusion_matrix' in metrics:
            figures.append(self.plot_confusion_matrix(metrics['confusion_matrix']))

        return figures

    def save_figure(self, fig, filename, format='html'):
        """
        Guarda una figura en archivo

        Args:
            fig: Figura de Plotly
            filename: Nombre del archivo
            format: Formato ('html', 'png', 'jpg')
        """
        if format == 'html':
            fig.write_html(filename)
        elif format == 'png':
            fig.write_image(filename)
        elif format == 'jpg':
            fig.write_image(filename)

        print(f"✓ Gráfico guardado en: {filename}")
