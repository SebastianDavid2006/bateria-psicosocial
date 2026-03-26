import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- FORZAR RUTA PARA QUE ENCUENTRE UTILS ---
# Esto ayuda a que el archivo reconozca la carpeta 'utils' que está al lado
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from utils.extractor import extraer_subdimension
except ImportError:
    # Si falla el anterior, intentamos una ruta alternativa
    from app.utils.extractor import extraer_subdimension

def render_explorador_dinamico(df_raw, categoria, COLORES_RIESGO, consultar_gemini):
    st.markdown("---")
    st.header(f"🎯 Explorador de Dimensiones: {categoria}")
    
    if st.button("✖️ Cerrar Explorador"):
        st.session_state['detalle_seleccionado'] = None
        st.rerun()

    # Mapeo de sub-dimensiones
    sub_dimensiones_dict = {
        "INTRALABORAL": ["Demandas emocionales", "Demandas de jornada laboral"],
        "EXTRALABORAL": ["Desplazamiento vivienda trabajo vivienda", "Características de la vivienda"],
        "ESTRÉS": ["Dolores en el cuello y espalda o tensión", "Problemas gastrointestinales"]
    }

    opciones = sub_dimensiones_dict.get(categoria, [])
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        dim_especifica = st.selectbox(f"Seleccione la dimensión de {categoria}:", opciones)
    with col_f2:
        modo_riesgo = st.toggle("Enfatizar Riesgo Crítico")

    # Extraemos datos reales del Excel
    df_dim = extraer_subdimension(df_raw, dim_especifica)
    
    # Calculamos porcentajes
    total = df_dim['Valor'].sum()
    df_dim['Porcentaje'] = (df_dim['Valor'] / total * 100) if total > 0 else 0

    if modo_riesgo:
        df_dim = df_dim[df_dim["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]

    # Gráfica
    fig_dim = px.bar(df_dim, x='Nivel', y='Porcentaje', color='Nivel', 
                     color_discrete_map=COLORES_RIESGO, text_auto='.2f', height=400)
    st.plotly_chart(fig_dim, use_container_width=True)

    # Botón de IA
    if st.button(f"✨ Generar Plan con IA para {dim_especifica}"):
        with st.spinner("Consultando a Gemini..."):
            val_muy_alto = df_dim[df_dim["Nivel"] == "Riesgo muy alto"]["Porcentaje"].sum()
            p_ia = f"Genera 3 acciones de intervención para la dimensión '{dim_especifica}' con un {val_muy_alto:.1f}% de riesgo muy alto."
            st.markdown(consultar_gemini(p_ia))