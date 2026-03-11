import streamlit as st
import pandas as pd
import plotly.express as px

def render_header() -> None:
    """Renderiza el título y subtítulo de la aplicación."""
    st.title("🛒 Análisis de Retención de Clientes (Churn)")
    st.markdown("Dashboard interactivo para explorar los factores clave que impulsan el abandono de clientes en el E-commerce.")


def render_sidebar_filters(col_filtros) -> str:
    """Renderiza el componente de filtros en la columna derecha de la estructura principal."""
    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        opcion = st.radio(
            "Ver datos de:",
            ("Todos", "Activos", "Perdidos")
        )
    return opcion


def render_kpis(df_filtrado: pd.DataFrame, df_original: pd.DataFrame, estado_filtro: str) -> None:
    """Construye y renderiza la fila superior de métricas clave (Z-Pattern Top)."""
    st.markdown("### 📌 Métricas Clave")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric(label="Total de Clientes", value=f"{len(df_filtrado):,}")
        
    with kpi2:
        if 'Lifetime_Value' in df_filtrado.columns and not df_filtrado.empty:
            ltv_promedio = df_filtrado['Lifetime_Value'].mean()
            st.metric(label="LTV Promedio ($)", value=f"${ltv_promedio:,.2f}")
        else:
            st.metric(label="LTV Promedio", value="N/A")
            
    with kpi3:
        if estado_filtro == "Todos" and not df_original.dropna(subset=['Churned']).empty:
             tasa_churn = df_original['Churned'].mean() * 100
             st.metric(label="Tasa de Churn Global (%)", value=f"{tasa_churn:.2f}%")
        elif estado_filtro == "Activos":
             st.metric(label="Tasa de Churn Actual", value="0.00%")
        elif estado_filtro == "Perdidos":
             st.metric(label="Tasa de Churn Actual", value="100.00%")
             
    st.markdown("---")


def render_impact_chart(df: pd.DataFrame) -> None:
    """Renderiza el gráfico de barras horizontales evaluando la correlación de impacto (Z-Pattern Centro)."""
    st.markdown("### 🎯 Top 3 Variables que influyen en el Churn")
    st.markdown("Impacto relativo de las acciones del usuario en la retención (basado en correlación global).")
    
    correlaciones = []
    variables_clave = ['Customer_Service_Calls', 'Cart_Abandonment_Rate', 'Pages_Per_Session']
    
    for var in variables_clave:
        if var in df.columns:
            res = df['Churned'].corr(df[var])
            correlaciones.append(res)
        else:
            correlaciones.append(0)
            
    df_impacto = pd.DataFrame({
        "Variable": ["☎️ Llamadas a Soporte", "🛒 Tasa de Abandono de Carrito", "📄 Páginas por Sesión"],
        "Correlación": correlaciones
    })
    
    df_impacto = df_impacto.sort_values(by="Correlación", ascending=True)
    df_impacto['Impacto en Retención'] = df_impacto['Correlación'].apply(
        lambda x: "Negativa (Aumenta Churn)" if x > 0 else "Positiva (Reduce Churn)"
    )
    
    fig_impacto = px.bar(
        df_impacto,
        x="Correlación",
        y="Variable",
        orientation='h',
        color="Impacto en Retención",
        color_discrete_map={
            "Positiva (Reduce Churn)": "#1f77b4",
            "Negativa (Aumenta Churn)": "#d62728"
        },
        text_auto='.2f', 
        hover_data={"Correlación": ':.3f'} 
    )
    
    fig_impacto.update_layout(
        xaxis_title="Fuerza de la Correlación (Impacto)",
        yaxis_title="",
        showlegend=True,
        legend_title="Tipo de Impacto",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) 
    )
    
    st.plotly_chart(fig_impacto, use_container_width=True)
    st.markdown("---")


def render_bottom_section(df_filtrado: pd.DataFrame) -> None:
    """Renderiza el Boxplot y el Panel de Conclusiones inferior (Z-Pattern Bottom)."""
    col_boxplot, col_conclusiones = st.columns([1.5, 1])
    
    with col_boxplot:
        st.markdown("#### Distribución del Lifetime Value (Real)")
        
        if 'Lifetime_Value' in df_filtrado.columns and 'Churned' in df_filtrado.columns:
            df_bp = df_filtrado.copy()
            df_bp['Estado'] = df_bp['Churned'].map({0: 'Activos', 1: 'Perdidos'})
            
            fig_bp = px.box(
                df_bp,
                x="Estado",
                y="Lifetime_Value",
                color="Estado",
                color_discrete_map={
                    "Activos": "#2ca02c", 
                    "Perdidos": "#ff7f0e" 
                },
                points="outliers", 
                hover_data=["Lifetime_Value"]
            )
            
            fig_bp.update_layout(
                xaxis_title="",
                yaxis_title="Lifetime Value Registrado ($)",
                showlegend=False 
            )
            
            st.plotly_chart(fig_bp, use_container_width=True)
            
    with col_conclusiones:
        st.markdown("#### 💡 Conclusiones del Análisis")
        st.info(
            "**Resumen de Riesgos y Retención:**\n\n"
            "A mayor número de llamadas a soporte técnico y aumento en la tasa de carritos abandonados, "
            "el cliente tiene una **alta probabilidad de irse** (Churn).\n\n"
            "Por el contrario, fomentar la navegación extendida por múltiples páginas *(Pages Per Session)* "
            "representa nuestra mejor herramienta intrínseca de retención.\n\n"
            "Adicionalmente, se observa que los clientes que perdemos tenían, históricamente, "
            "un **Lifetime Value significativamente menor** en comparación con los que permanecen activos.",
            icon="📊"
        )
