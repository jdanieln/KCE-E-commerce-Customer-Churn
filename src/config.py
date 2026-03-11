import streamlit as st

def setup_page():
    """Configura las propiedades iniciales de la página del dashboard."""
    st.set_page_config(
        page_title="Dashboard E-commerce: Retención",
        page_icon="🛒",
        layout="wide"
    )

def apply_custom_css():
    """Aplica estilos CSS personalizados a la aplicación que respetan temas claros y oscuros."""
    st.markdown("""
        <style>
        /* Estilo para las tarjetas de KPIs que se adapta al modo claro/oscuro */
        div[data-testid="metric-container"] {
            background-color: var(--background-color);
            border: 1px solid var(--secondary-background-color);
            padding: 5% 5% 5% 10%;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)
