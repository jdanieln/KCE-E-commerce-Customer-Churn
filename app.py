import streamlit as st
# Importaciones relativas desde la estructura modular 'src'
from src.config import setup_page, apply_custom_css
from src.data_processor import load_and_clean_data, filter_data_by_status
from src.ui_components import (
    render_header, 
    render_sidebar_filters, 
    render_kpis, 
    render_impact_chart, 
    render_bottom_section
)

# 1. Ejecutar las configuraciones iniciales
setup_page()
apply_custom_css()

# 2. Renderizar la cabecera (Título y Subtítulo)
render_header()

# 3. Cargar y preparar los datos delegando a la capa de procesamiento
df = load_and_clean_data()

# 4. Lógica de Interfaz y layout
if not df.empty:
    
    # Creamos un layout de 2 columnas principales: 80% para gráficos, 20% para filtros a la derecha
    col_main, col_filtros = st.columns([4, 1])
    
    # Renderizar el control de filtros
    opcion_filtro = render_sidebar_filters(col_filtros)
    
    # Filtrar el DataFrame según la selección del usuario
    df_filtrado = filter_data_by_status(df, opcion_filtro)
    
    with col_main:
        # Fila superior de métricas dinámicas
        render_kpis(df_filtrado, df, opcion_filtro)
        
        # Gráfico central (Calculado sobre el general para consistencia en la correlación)
        render_impact_chart(df)
        
        # Fila inferior: Boxplots y conclusiones
        render_bottom_section(df_filtrado)
