import streamlit as st
import pandas as pd
import plotly.express as px
# Importamos la lógica y el orden desde tu carpeta utils
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

    # --- Pestañas A y B (Valores Absolutos) ---
    for tab, data_dict, sufijo in zip([t1, t2], [data_a, data_b], ["A", "B"]):
        with tab:
            cols = st.columns(3)
            for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
                with cols[i]:
                    fig = px.bar(data_dict[dim], x='Nivel', y='Valor', title=f"{dim} {sufijo}",
                                 color='Nivel', color_discrete_map=COLORES_RIESGO, text_auto=True)
                    st.plotly_chart(fig, use_container_width=True)

    # --- Pestaña Consolidado ---
    with t3:
        st.subheader("⚠️ Análisis de Riesgo Crítico (Consolidado)")
        m_cols = st.columns(3)
        lista_final = []
        
        for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
            df_c = data_a[dim].copy()
            df_c["Valor"] = data_a[dim]["Valor"] + data_b[dim]["Valor"]
            
            total = df_c["Valor"].sum()
            df_c["Porc_Txt"] = df_c["Valor"].apply(lambda x: f"{(x/total*100):.1f}%" if total > 0 else "0%")
            lista_final.append(df_c)
            
            # Cálculo de Impacto Crítico (Alto + Muy Alto)
            suma_critica = df_c[df_c["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]["Valor"].sum()
            porc_critico = (suma_critica / total * 100) if total > 0 else 0
            
            with m_cols[i]:
                st.metric(f"Impacto Crítico {dim}", f"{porc_critico:.1f}%")
                st.progress(min(porc_critico/100, 1.0))

        st.markdown("---")
        st.subheader("📊 Gráficos por Dimensión (%)")
        g_cols = st.columns(3)
        for i, dim in enumerate(["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]):
            fig = px.bar(lista_final[i], x='Nivel', y='Valor', title=f"{dim} (A+B)",
                         color='Nivel', color_discrete_map=COLORES_RIESGO, text="Porc_Txt")
            fig.update_layout(yaxis_title="Cantidad de Personas")
            g_cols[i].plotly_chart(fig, use_container_width=True)

        # --- SECCIÓN RESTAURADA: RESULTADO GLOBAL ---
        st.markdown("---")
        st.subheader("📈 Resultado Global de la Empresa")
        
        # Agrupamos todos los valores de todas las dimensiones
        df_global = pd.concat(lista_final).groupby('Nivel')['Valor'].sum().reindex(ORDEN_RIESGO).reset_index().fillna(0)
        total_global = df_global['Valor'].sum()
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            # Gráfica de Dona (Pie Chart con hole)
            fig_pie = px.pie(df_global, values='Valor', names='Nivel', hole=0.5,
                             color='Nivel', color_discrete_map=COLORES_RIESGO)
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.write("**Detalle por Número de Personas:**")
            for _, row in df_global.iterrows():
                porcentaje = (row['Valor'] / total_global * 100) if total_global > 0 else 0
                st.write(f"**{row['Nivel']}**: {porcentaje:.1f}% ({int(row['Valor'])} respuestas)")