import streamlit as st
import pandas as pd
import plotly.express as px
# Importamos tu motor lógico
from utils.extractor import extraer_datos_psicosocial, ORDEN_RIESGO

st.set_page_config(page_title="Batería Psicosocial AI", layout="wide")

COLORES_RIESGO = {
    "Sin Riesgo": "#2ECC71", "Riesgo bajo": "#ABEBC6", "Riesgo medio": "#F4D03F",
    "Riesgo alto": "#E67E22", "Riesgo muy alto": "#C0392B", "Dato perdido": "#D3D3D3"
}

st.title("🛡️ Sistema de Análisis Psicosocial")

archivo = st.file_uploader("Cargar reporte Excel", type=["xlsx"])

if archivo:
    df_raw = pd.read_excel(archivo, sheet_name="Gráficas", header=None)
    data_a = extraer_datos_psicosocial(df_raw, "A")
    data_b = extraer_datos_psicosocial(df_raw, "B")

    t1, t2, t3 = st.tabs(["📊 Jefes", "📊 Operativos", "🌐 Consolidado"])

    # --- Lógica de pestañas A y B (Valores absolutos) ---
    for tab, data_dict, sufijo in zip([t1, t2], [data_a, data_b], ["A", "B"]):
        with tab:
            cols = st.columns(3)
            for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
                with cols[i]:
                    fig = px.bar(data_dict[dim], x='Nivel', y='Valor', title=f"{dim} {sufijo}",
                                 color='Nivel', color_discrete_map=COLORES_RIESGO, text_auto=True)
                    st.plotly_chart(fig, use_container_width=True)

    # --- Lógica de Consolidado (Porcentajes) ---
    with t3:
        lista_final = []
        m_cols = st.columns(3)
        for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
            df_c = data_a[dim].copy()
            df_c["Valor"] = data_a[dim]["Valor"] + data_b[dim]["Valor"]
            
            total = df_c["Valor"].sum()
            df_c["Porc_Txt"] = df_c["Valor"].apply(lambda x: f"{(x/total*100):.1f}%" if total > 0 else "0%")
            lista_final.append(df_c)
            
            # Métrica de Riesgo Crítico
            crit = (df_c[df_c["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]["Valor"].sum() / total * 100) if total > 0 else 0
            m_cols[i].metric(f"Impacto Crítico {dim}", f"{crit:.1f}%")

        st.markdown("---")
        g_cols = st.columns(3)
        for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
            fig = px.bar(lista_final[i], x='Nivel', y='Valor', title=f"{dim} (Consolidado)",
                         color='Nivel', color_discrete_map=COLORES_RIESGO, text="Porc_Txt")
            g_cols[i].plotly_chart(fig, use_container_width=True)