import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px

# --- 1. CONFIGURACIÓN DE RUTAS ---
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# --- 2. IMPORTS DE TUS MÓDULOS ---
try:
    from utils.extractor import extraer_datos_psicosocial
    from utils.consultar_gemini import consultar_gemini
    from components.tabs_view import render_tabs
    from components.explorador import render_explorador_dinamico
except ModuleNotFoundError as e:
    st.error(f"❌ Error al cargar módulos internos: {e}")
    st.stop()

# --- 3. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Batería Psicosocial AI", layout="wide")

# --- 4. CSS Y ESTILOS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

path_css = os.path.join(root_path, "styles", "custom.css")
local_css(path_css)

# Constantes Globales
ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]
COLORES_RIESGO = {
    "Sin Riesgo": "#2ECC71", "Riesgo bajo": "#ABEBC6", "Riesgo medio": "#F4D03F",
    "Riesgo alto": "#E67E22", "Riesgo muy alto": "#C0392B", "Dato perdido": "#D3D3D3"
}

if 'detalle_seleccionado' not in st.session_state:
    st.session_state['detalle_seleccionado'] = None

# --- FUNCIONES DE APOYO PARA CONSOLIDADO ---
def sumar_formas(d_a, d_b, clave):
    df_sum = d_a[clave].copy()
    df_sum['Valor'] = d_a[clave]['Valor'] + d_b[clave]['Valor']
    return df_sum

def obtener_riesgo_critico(df):
    critico = df[df["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]["Valor"].sum()
    total = df["Valor"].sum()
    return (critico / total * 100) if total > 0 else 0

# --- 5. INTERFAZ PRINCIPAL ---
st.title("🛡️ Sistema de Análisis Psicosocial")

archivo = st.file_uploader("Cargar reporte Excel (Hoja 'Gráficas')", type=["xlsx"])

if archivo is not None:
    try:
        df_raw = pd.read_excel(archivo, sheet_name="Gráficas", header=None)
        data_a = extraer_datos_psicosocial(df_raw, "A")
        data_b = extraer_datos_psicosocial(df_raw, "B")

        global_intra = sumar_formas(data_a, data_b, "INTRALABORAL")
        global_extra = sumar_formas(data_a, data_b, "EXTRALABORAL")
        global_estres = sumar_formas(data_a, data_b, "ESTRÉS")

        st.subheader("🚨 Dimensiones Críticas Detectadas")
        c1, c2, c3 = st.columns(3)
        with c1:
            val = obtener_riesgo_critico(global_intra)
            st.error(f"🆘 **Intralaboral**: {val:.1f}% en Riesgo Crítico")
        with c2:
            val = obtener_riesgo_critico(global_extra)
            st.error(f"🆘 **Extralaboral**: {val:.1f}% en Riesgo Crítico")
        with c3:
            val = obtener_riesgo_critico(global_estres)
            st.warning(f"⚠️ **Síntomas Estrés**: {val:.1f}% Nivel Alto")

        t1, t2, t3 = st.tabs(["📊 Jefes (A)", "📊 Operativos (B)", "🌐 Consolidado Global"])
        render_tabs(data_a, data_b, t1, t2, t3, COLORES_RIESGO)

        with t3:
            st.markdown("### 📈 Resumen Ejecutivo de la Organización")
            
            # --- TARJETAS SUPERIORES ---
            col_t1, col_t2, col_t3 = st.columns(3)
            tarjeta_style = """
            <div style="background: linear-gradient(135deg, {color} 0%, {color}CC 100%); 
                        padding: 25px; border-radius: 15px; color: white; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h5 style="margin:0; opacity: 0.9; font-size: 14px;">{titulo}</h5>
                <h2 style="margin:10px 0; font-size: 32px; font-weight: bold;">{porcentaje:.1f}%</h2>
                <p style="margin:0; font-size: 12px; opacity: 0.8;">Riesgo Crítico (Alto + Muy Alto)</p>
            </div>
            """
            with col_t1: st.markdown(tarjeta_style.format(titulo="INTRALABORAL", porcentaje=obtener_riesgo_critico(global_intra), color="#C0392B"), unsafe_allow_html=True)
            with col_t2: st.markdown(tarjeta_style.format(titulo="EXTRALABORAL", porcentaje=obtener_riesgo_critico(global_extra), color="#E67E22"), unsafe_allow_html=True)
            with col_t3: st.markdown(tarjeta_style.format(titulo="ESTRÉS", porcentaje=obtener_riesgo_critico(global_estres), color="#2E86C1"), unsafe_allow_html=True)

            st.markdown("---")
            
            # --- NUEVA SECCIÓN: ESTADÍSTICAS GENERALES (A+B) EN % ---
            st.subheader("📊 Distribución Porcentual por Dimensión (A+B)")
            col_g1, col_g2, col_g3 = st.columns(3)
            
            dims_globales = [
                ("Intralaboral", global_intra, col_g1),
                ("Extralaboral", global_extra, col_g2),
                ("Estrés", global_estres, col_g3)
            ]
            
            for nombre, df_g, columna in dims_globales:
                with columna:
                    # Calculamos el porcentaje para esta dimensión específica
                    total_dim = df_g['Valor'].sum()
                    df_g_pct = df_g.copy()
                    df_g_pct['Porcentaje'] = (df_g_pct['Valor'] / total_dim * 100)
                    
                    fig_bar = px.bar(
                        df_g_pct, 
                        x='Porcentaje', 
                        y='Nivel', 
                        orientation='h',
                        color='Nivel', 
                        color_discrete_map=COLORES_RIESGO,
                        text=df_g_pct['Porcentaje'].apply(lambda x: f'{x:.1f}%'),
                        title=f"Distribución {nombre}"
                    )
                    
                    fig_bar.update_layout(
                        showlegend=False, 
                        height=280, 
                        margin=dict(l=0, r=40, t=40, b=0),
                        xaxis_title="", 
                        yaxis_title="", 
                        xaxis_visible=False,
                        # Asegura que el texto del % siempre quepa
                        uniformtext_minsize=10, 
                        uniformtext_mode='hide'
                    )
                    fig_bar.update_traces(textposition='outside', cliponaxis=False)
                    st.plotly_chart(fig_bar, use_container_width=True, key=f"global_pct_{nombre}")

            st.markdown("---")
            st.subheader("🍩 Distribución y Volumen de Riesgos")

            # Datos para Dona
            df_consolidado = pd.concat([global_intra, global_extra, global_estres]).groupby("Nivel")["Valor"].sum().reset_index()
            df_consolidado['Nivel'] = pd.Categorical(df_consolidado['Nivel'], categories=ORDEN_RIESGO, ordered=True)
            df_consolidado = df_consolidado.sort_values('Nivel')
            
            total_respuestas = int(df_consolidado['Valor'].sum())
            total_personas = int(global_estres['Valor'].sum())

            col_dona, col_lista = st.columns([2, 1])

            with col_dona:
                fig_dona = px.pie(df_consolidado, values='Valor', names='Nivel', hole=0.6,
                                 color='Nivel', color_discrete_map=COLORES_RIESGO)
                fig_dona.update_traces(textposition='inside', textinfo='percent', textfont_size=16)
                fig_dona.add_annotation(
                    text=f"<span style='color:white; text-shadow: 2px 2px 4px #000000;'><b>{total_personas}</b><br>Encuestados</span>",
                    showarrow=False, font=dict(size=22), x=0.5, y=0.5
                )
                fig_dona.update_layout(showlegend=False, height=450, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_dona, use_container_width=True)

            with col_lista:
                st.markdown("#### 📊 Conteo de Respuestas")
                for _, row in df_consolidado.iterrows():
                    color = COLORES_RIESGO.get(row['Nivel'], "#333")
                    st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; 
                                    padding: 10px; border-bottom: 1px solid #333; margin-bottom: 5px;
                                    background: rgba(255,255,255,0.02); border-radius: 5px;">
                            <span style="border-left: 5px solid {color}; padding-left: 15px; color: #E0E0E0; font-size: 14px;">
                                {row['Nivel']}
                            </span>
                            <span style="background: {color}33; color: white; padding: 2px 12px; border-radius: 15px; 
                                        font-weight: bold; border: 1px solid {color}; font-size: 14px;">
                                {int(row['Valor'])}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top: 25px; padding: 20px; 
                                background: linear-gradient(135deg, #2c3e50 0%, #000000 100%); 
                                border-radius: 12px; border: 1px solid #444; text-align: center;">
                        <p style="margin:0; color: #aaa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
                            Total Respuestas Analizadas
                        </p>
                        <h1 style="margin:0; color: white; font-size: 42px; font-weight: 800;">{total_respuestas}</h1>
                    </div>
                """, unsafe_allow_html=True)

        if st.session_state['detalle_seleccionado']:
            sel_clave = st.session_state['detalle_seleccionado']
            categoria = sel_clave.split("_")[0] 
            render_explorador_dinamico(df_raw, categoria, COLORES_RIESGO, consultar_gemini)

    except Exception as e:
        st.error(f"Error en procesamiento.")
        st.exception(e)