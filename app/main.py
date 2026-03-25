import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from google import genai 

# Añadir la raíz del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils.extractor import extraer_datos_psicosocial, ORDEN_RIESGO

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyCvjEW0fLeBgWFRJUq8m_8m10NDoxDZB3o"
client = genai.Client(api_key=API_KEY)

def consultar_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error en la IA: {e}"

st.set_page_config(page_title="Batería Psicosocial AI", layout="wide")

# --- CARGA DE CSS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

path_css = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
local_css(path_css)

# --- CONFIGURACIÓN DE COLORES ---
COLORES_RIESGO = {
    "Sin Riesgo": "#2ECC71", "Riesgo bajo": "#ABEBC6", "Riesgo medio": "#F4D03F",
    "Riesgo alto": "#E67E22", "Riesgo muy alto": "#C0392B", "Dato perdido": "#D3D3D3"
}

st.title("🛡️ Sistema de Análisis Psicosocial")

archivo = st.file_uploader("Cargar reporte Excel", type=["xlsx"])

if 'analisis_dict' not in st.session_state:
    st.session_state['analisis_dict'] = {}

if archivo is not None:
    try:
        df_raw = pd.read_excel(archivo, sheet_name="Gráficas", header=None)
        data_a = extraer_datos_psicosocial(df_raw, "A")
        data_b = extraer_datos_psicosocial(df_raw, "B")

        t1, t2, t3 = st.tabs(["📊 Jefes (A)", "📊 Operativos (B)", "🌐 Consolidado"])

        # === Pestañas A y B (Gráficos con Respaldo de Participación) ===
        for tab, data_dict, sufijo in zip([t1, t2], [data_a, data_b], ["A", "B"]):
            with tab:
                # --- AGREGADO: CÁLCULO DE PARTICIPACIÓN ---
                # Se calcula sumando los valores de una dimensión (ej. ESTRÉS)
                n_total = int(data_dict["ESTRÉS"]["Valor"].sum())
                st.info(f"📋 **Muestra de respaldo:** {n_total} personas completaron esta encuesta.")
                
                dimensiones = ["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]
                cols = st.columns(3)
                
                for i, dim in enumerate(dimensiones):
                    clave = f"{dim}_{sufijo}"
                    with cols[i]:
                        fig = px.bar(data_dict[dim], x='Nivel', y='Valor', title=f"{dim} ({sufijo})",
                                     color='Nivel', color_discrete_map=COLORES_RIESGO, text_auto=True)
                        
                        # --- SOLUCIÓN A LA OPACIDAD ---
                        fig.update_traces(
                            selected_marker_opacity=1,
                            unselected_marker_opacity=1
                        )
                        fig.update_layout(
                            showlegend=False,
                            clickmode='event+select',
                            hovermode="x"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key=f"chart_{clave}")
                        
                        if st.button(f"🔍 Analizar {dim}", key=f"btn_{clave}"):
                            with st.spinner("IA analizando..."):
                                stats = data_dict[dim].to_dict(orient='records')
                                prompt = f"Analiza estos datos de riesgo {dim} para {sufijo}: {stats}. Dame 3 hallazgos clave muy breves."
                                st.session_state['analisis_dict'][clave] = consultar_gemini(prompt)
                        
                        if clave in st.session_state['analisis_dict']:
                            st.markdown(f"""
                                <div class="resultado-ia-columna">
                                    <strong>🔍 Análisis de IA:</strong><br/>
                                    {st.session_state['analisis_dict'][clave]}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("Limpiar", key=f"clear_{clave}"):
                                del st.session_state['analisis_dict'][clave]
                                st.rerun()

        # === Pestaña Consolidado ===
        with t3:
            st.markdown('<div class="consolidado-panel">', unsafe_allow_html=True)
            st.subheader("⚠️ Análisis de Riesgo Crítico (Consolidado)")
            
            m_cols = st.columns(3)
            lista_final = []
            datos_para_plan = {} 
            
            for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
                df_c = data_a[dim].copy()
                df_c["Valor"] = data_a[dim]["Valor"] + data_b[dim]["Valor"]
                total = df_c["Valor"].sum()
                df_c["Porc_Txt"] = df_c["Valor"].apply(lambda x: f"{(x/total*100):.1f}%" if total > 0 else "0%")
                lista_final.append(df_c)
                
                suma_critica = df_c[df_c["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]["Valor"].sum()
                porc_critico = (suma_critica / total * 100) if total > 0 else 0
                datos_para_plan[dim] = f"{porc_critico:.1f}%"
                
                with m_cols[i]:
                    st.markdown(f"""
                        <div class="metric-card-custom">
                            <div class="metric-label-custom">Impacto Crítico {dim}</div>
                            <div class="metric-value-custom">{porc_critico:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.progress(min(porc_critico/100, 1.0))
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### 🚀 Estrategia de Intervención Inteligente")
            if st.button("✨ Generar Plan de Acción con Gemini", type="primary"):
                with st.spinner("Generando..."):
                    prompt_plan = f"Genera un plan estratégico para: {datos_para_plan}. Formatea con negritas: 1. Intervención, 2. Actividades, 3. KPI."
                    respuesta_plan = consultar_gemini(prompt_plan)
                    st.success("Plan Estratégico Generado:")
                    st.markdown(respuesta_plan)

            st.markdown("---")
            st.subheader("📊 Gráficos por Dimensión Consolidada (%)")
            g_cols = st.columns(3)
            for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
                fig_c = px.bar(lista_final[i], x='Nivel', y='Valor', title=f"{dim} (Consolidado)",
                             color='Nivel', color_discrete_map=COLORES_RIESGO, 
                             category_orders={"Nivel": ORDEN_RIESGO}, text="Porc_Txt")
                
                fig_c.update_traces(selected_marker_opacity=1, unselected_marker_opacity=1)
                fig_c.update_layout(showlegend=False, yaxis_title="Personas")
                g_cols[i].plotly_chart(fig_c, use_container_width=True)

            # --- SECCIÓN: Resultado Global de la Población ---
            # --- SECCIÓN: Resultado Global de la Población ---
            st.markdown("---")
            st.subheader("📈 Resultado Global de la Población")
            
            # 1. Agrupamos todo para los porcentajes del gráfico
            df_g_all = pd.concat(lista_final).groupby('Nivel')['Valor'].sum().reindex(ORDEN_RIESGO).reset_index().fillna(0)
            
            # 2. LÓGICA DE POBLACIÓN REAL: 
            # Sumamos solo una dimensión (ej. la primera en lista_final) para no triplicar personas
            t_g_real = lista_final[0]['Valor'].sum() 
            
            c1, c2 = st.columns([1.5, 1])
            with c1:
                # El gráfico de dona usa df_g_all para mostrar la tendencia de TODAS las respuestas
                fig_p = px.pie(df_g_all, values='Valor', names='Nivel', hole=0.5, 
                               color='Nivel', color_discrete_map=COLORES_RIESGO)
                
                fig_p.update_traces(textinfo='percent+label', opacity=1)
                
                # Anotación con la N real de personas (A + B)
                fig_p.add_annotation(
                    text=f"Población:<br><b>{int(t_g_real)}</b><br>Personas",
                    showarrow=False,
                    font_size=16,
                    font_color="white",
                    x=0.5, y=0.5
                )
                
                st.plotly_chart(fig_p, use_container_width=True)
                
            with c2:
                st.markdown(f"**Participación Real (A + B):** `{int(t_g_real)} colaboradores` 👥")
                st.write("Desglose de niveles basado en el total de respuestas recibidas:")
                st.markdown("---")
                
                # Para el desglose lateral, usamos el total de respuestas (que es t_g_real * 3)
                t_respuestas = df_g_all['Valor'].sum()
                for _, r in df_g_all.iterrows():
                    p = (r['Valor']/t_respuestas*100) if t_respuestas > 0 else 0
                    st.write(f"**{r['Nivel']}**: {p:.1f}% ({int(r['Valor'])} menciones)")

    except Exception as e:
        st.error(f"Error técnico: {e}")