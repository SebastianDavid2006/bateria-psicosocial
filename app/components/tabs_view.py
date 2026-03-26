import streamlit as st
import plotly.express as px

def render_tabs(data_a, data_b, t1, t2, t3, COLORES_RIESGO):
    # === Pestañas A y B (Jefes y Operativos) ===
    # Solo trabajamos en t1 y t2 aquí
    for tab, data_dict, sufijo in zip([t1, t2], [data_a, data_b], ["A", "B"]):
        with tab:
            n_total = int(data_dict["ESTRÉS"]["Valor"].sum())
            st.info(f"📋 **Muestra de respaldo:** {n_total} personas completaron la encuesta Forma {sufijo}.")
            
            dimensiones = ["INTRALABORAL", "EXTRALABORAL", "ESTRÉS"]
            cols = st.columns(3)
            
            for i, dim in enumerate(dimensiones):
                clave = f"{dim}_{sufijo}"
                with cols[i]:
                    # Gráfica de barras individual
                    fig = px.bar(
                        data_dict[dim], 
                        x='Nivel', 
                        y='Valor', 
                        title=f"{dim} ({sufijo})",
                        color='Nivel', 
                        color_discrete_map=COLORES_RIESGO, 
                        text_auto='.0f'
                    )
                    
                    fig.update_layout(
                        showlegend=False, 
                        height=350,
                        margin=dict(l=20, r=20, t=40, b=20),
                        xaxis_title="",
                        yaxis_title="Cantidad"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{clave}")
                    
                    # Botón para activar el explorador dinámico
                    if st.button(f"🔍 Detalles {dim}", key=f"btn_det_{clave}", use_container_width=True):
                        st.session_state['detalle_seleccionado'] = clave
                        st.rerun()

    # === Pestaña Consolidado (Silenciosa) ===
    # IMPORTANTE: No escribimos nada aquí para evitar duplicados con el main.py
    if t3 is not None:
        with t3:
            pass