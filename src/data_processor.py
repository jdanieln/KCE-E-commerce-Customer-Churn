import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data(file_path: str = "data/ecommerce_customer_churn_dataset.csv") -> pd.DataFrame:
    """Carga el dataset desde el disco, reconstruye las variables aplicando la 
    escala inversa y limpia los nulos requeridos de forma segura."""
    try:
        # Carga del dataset Z-score (estandarizado)
        df = pd.read_csv(file_path)
        
        # Parámetros hipotéticos de negocio para revertir el StandardScaler
        parametros_reconstruccion = {
            'Lifetime_Value': {'mean': 850.50, 'std': 320.25},            # Valor histórico en USD
            'Customer_Service_Calls': {'mean': 2.5, 'std': 1.5},          # Cantidad de llamadas
            'Cart_Abandonment_Rate': {'mean': 0.65, 'std': 0.18},         # Tasa porcentual (0 a 1)
            'Pages_Per_Session': {'mean': 6.5, 'std': 2.8},               # Páginas visitadas
        }
        
        # Proceso de reconstrucción (Inverse Transform)
        for col, params in parametros_reconstruccion.items():
            if col in df.columns:
                df[col] = (df[col] * params['std']) + params['mean']
                
                # Clipper para evitar realidades ilógicas (valores en -0)
                if col in ['Lifetime_Value', 'Customer_Service_Calls', 'Pages_Per_Session', 'Cart_Abandonment_Rate']:
                    df[col] = df[col].clip(lower=0)
                    
                # Variables discretas que deben ser enteros
                if col in ['Customer_Service_Calls', 'Pages_Per_Session']:
                    df[col] = df[col].round().astype(int)
        
        # Relleno de nulos según reglas de negocio
        if 'Churned' in df.columns:
            df['Churned'] = df['Churned'].fillna(0).astype(int)
            
        if 'Lifetime_Value' in df.columns:
            # Rellenar con la mediana local ya reconstruida
            mediana_ltv = df['Lifetime_Value'].median()
            df['Lifetime_Value'] = df['Lifetime_Value'].fillna(mediana_ltv)
            
        return df
        
    except FileNotFoundError:
        st.error(f"⚠️ No se encontró el archivo '{file_path}'. Por favor, colócalo en el directorio raíz.")
        return pd.DataFrame()


def filter_data_by_status(df: pd.DataFrame, status: str) -> pd.DataFrame:
    """Filtra los datos del dashboard interactivo basado en la selección del usuario."""
    if status == "Activos":
        return df[df['Churned'] == 0]
    elif status == "Perdidos":
        return df[df['Churned'] == 1]
    return df.copy() # Opción 'Todos'
