import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
import base64  # Necesario para procesar el logo

# --- 1. CONFIGURACIÓN DE RUTAS ---
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# --- 2. IMPORTS DE TUS MÓDULOS ---
try:
    from utils.extractor import extraer_datos_psicosocial, extraer_subdimension
    from utils.consultar_gemini import consultar_gemini
    from components.tabs_view import render_tabs
    from components.explorador import render_explorador_dinamico
except ModuleNotFoundError as e:
    st.error(f"❌ Error al cargar módulos internos: {e}")
    st.stop()

@st.dialog("📊 Diagnóstico de Riesgo Psicosocial")
def mostrar_analisis_modal(titulo, contenido):
    st.write(f"### Análisis: {titulo}")
    
    # Contenedor con scroll por si la IA se extiende
    with st.container(height=400, border=False):
        st.markdown(contenido)
    
    if st.button("✅ Entendido", use_container_width=True):
        st.rerun()

# --- 3. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Batería Psicosocial AI", layout="wide")

# --- 4. CSS Y ESTILOS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown("""
            <style>
            /* ⚠️ CSS CRÍTICO PARA DESENFOQUE TOTAL DE FONDO:
            Este selector avanzado detecta la presencia del modal 
            y aplica el efecto de desenfoque a TODA la vista de la aplicación de fondo.
            Se debe asegurar que el navegador soporta :has() (Chrome 105+, Safari 15.4+, Edge 105+).
            */
            :root:has(div[data-testid="stDialog"]) .stAppViewContainer {
                filter: blur(12px) !important; /* Aumentado a 12px para mayor contraste */
                transition: filter 0.3s ease-in-out; /* Animación suave al abrir/cerrar */
            }

            /* Aseguramos que el área oscura detrás del modal sea uniforme y 
            tape las distracciones si el navegador no soporta desenfoque total.
            */
            div[data-testid="stDialog"] {
                background-color: rgba(0, 0, 0, 0.75) !important; /* Oscurece la pantalla completa */
            }

            /* Ajustes estéticos al cuadro del diálogo para maximizar legibilidad 
            */
            div[data-testid="stDialog"] div[role="dialog"] {
                border-radius: 12px !important;
                background-color: #1a1c24 !important; /* Un tono más oscuro y sólido */
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
            }
            </style>
            """, unsafe_allow_html=True)

path_css = os.path.join(root_path, "styles", "custom.css")
local_css(path_css)

# Función para cargar y codificar el logo
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Constantes Globales
ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]
COLORES_RIESGO = {
    "Sin Riesgo": "#2ECC71", "Riesgo bajo": "#ABEBC6", "Riesgo medio": "#F4D03F",
    "Riesgo alto": "#E67E22", "Riesgo muy alto": "#C0392B", "Dato perdido": "#D3D3D3"
}

# Inicialización de estados
if 'detalle_seleccionado' not in st.session_state:
    st.session_state['detalle_seleccionado'] = None
if 'ver_subdimensiones_intra' not in st.session_state:
    st.session_state['ver_subdimensiones_intra'] = False

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

# Lógica del Logotipo
logo_path = os.path.join(root_path, "assets", "logo.png")
logo_base64 = get_base64_image(logo_path)

if logo_base64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 0px;">
            <img src="data:image/png;base64,{logo_base64}" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("🛡️ Sistema de Análisis Psicosocial")

archivo = st.file_uploader("Cargar reporte Excel (Hoja 'Gráficas')", type=["xlsx", "xlsb"])

if archivo is not None:
    try:
        # Detectar el motor según la extensión
        extension = archivo.name.split('.')[-1].lower()
        motor = "pyxlsb" if extension == "xlsb" else None # None usa el motor por defecto para .xlsx

        # Carga de datos base
        df_raw = pd.read_excel(archivo, sheet_name="Gráficas", header=None, engine=motor)
        data_a = extraer_datos_psicosocial(df_raw, "A")
        data_b = extraer_datos_psicosocial(df_raw, "B")

        global_intra = sumar_formas(data_a, data_b, "INTRALABORAL")
        global_extra = sumar_formas(data_a, data_b, "EXTRALABORAL")
        global_estres = sumar_formas(data_a, data_b, "ESTRÉS")

        # Render de Pestañas
        t1, t2, t3 = st.tabs(["📊 Jefes (A)", "📊 Operativos (B)", "🌐 Consolidado Global"])
        
        # Enviamos las pestañas al componente para que renderice el contenido base
        render_tabs(data_a, data_b, t1, t2, t3, COLORES_RIESGO)

        # --- LÓGICA DEL EXPLORADOR ---
        if st.session_state['detalle_seleccionado']:
            sel_clave = st.session_state['detalle_seleccionado']
            target_tab = t1 if "_A" in sel_clave else t2
            
            with target_tab:
                st.markdown("---")
                categoria = sel_clave.split("_")[0] 
                render_explorador_dinamico(df_raw, categoria, COLORES_RIESGO, consultar_gemini)

        # --- CONTENIDO ESPECÍFICO DE CONSOLIDADO (T3) ---
        with t3:
            # --- NUEVA SECCIÓN DE PARÁMETROS IA ---
            with st.expander("⚙️ Configuración del Plan de Acción (IA)"):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    formato_ia = st.selectbox("Formato", ["Lista de viñetas", "Párrafo ejecutivo", "Tabla de tareas"])
                    tono_ia = st.selectbox("Tono", ["Profesional y Técnico", "Directo y Ejecutivo", "Motivacional"])
                with col_p2:
                    max_palabras = st.slider("Extensión máxima (palabras)", 50, 500, 150)
            
            # Guardamos la configuración en un diccionario para la función
            config_ia = {
                "formato": formato_ia,
                "tono": tono_ia,
                "max_palabras": max_palabras
            }

            if not st.session_state['ver_subdimensiones_intra']:
                st.markdown("### 📈 Resumen Ejecutivo de la Organización")
                
                # --- TARJETAS SUPERIORES ---
                col_t1, col_t2, col_t3 = st.columns(3)
                tarjeta_style = """
                <div style="background: linear-gradient(135deg, {color} 0%, {color}CC 100%); 
                            padding: 25px; border-radius: 15px; color: white; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 10px;">
                    <h5 style="margin:0; opacity: 0.9; font-size: 14px;">{titulo}</h5>
                    <h2 style="margin:10px 0; font-size: 32px; font-weight: bold;">{porcentaje:.1f}%</h2>
                    <p style="margin:0; font-size: 12px; opacity: 0.8;">Riesgo Crítico (Alto + Muy Alto)</p>
                </div>
                """
                with col_t1: 
                    st.markdown(tarjeta_style.format(titulo="INTRALABORAL", porcentaje=obtener_riesgo_critico(global_intra), color="#C0392B"), unsafe_allow_html=True)
                
                with col_t2: 
                    st.markdown(tarjeta_style.format(titulo="EXTRALABORAL", porcentaje=obtener_riesgo_critico(global_extra), color="#E67E22"), unsafe_allow_html=True)
                
                with col_t3: 
                    st.markdown(tarjeta_style.format(titulo="ESTRÉS", porcentaje=obtener_riesgo_critico(global_estres), color="#2E86C1"), unsafe_allow_html=True)

                st.markdown("---")
                
                # --- GRÁFICAS PORCENTUALES ---
                st.subheader("📊 Distribución Porcentual por Dimensión (A+B)")
                col_g1, col_g2, col_g3 = st.columns(3)
                dims_globales = [("Intralaboral", global_intra, col_g1), ("Extralaboral", global_extra, col_g2), ("Estrés", global_estres, col_g3)]
                
                for nombre, df_g, columna in dims_globales:
                    with columna:
                        total_dim = df_g['Valor'].sum()
                        df_g_pct = df_g.copy()
                        df_g_pct['Porcentaje'] = (df_g_pct['Valor'] / total_dim * 100) if total_dim > 0 else 0
                        fig_bar = px.bar(df_g_pct, x='Porcentaje', y='Nivel', orientation='h',
                                       color='Nivel', color_discrete_map=COLORES_RIESGO,
                                       text=df_g_pct['Porcentaje'].apply(lambda x: f'{x:.1f}%'),
                                       title=f"Distribución {nombre}")
                        fig_bar.update_layout(showlegend=False, height=280, margin=dict(l=0, r=40, t=40, b=0),
                                           xaxis_visible=False, yaxis_title="", uniformtext_minsize=10, uniformtext_mode='hide')
                        fig_bar.update_traces(textposition='outside', cliponaxis=False)
                        st.plotly_chart(fig_bar, use_container_width=True, key=f"global_pct_{nombre}")
                        
                        # --- BOTONES DE ACCIÓN ---
                        c1, c2 = st.columns(2)
                        with c1:
                            if nombre == "Intralaboral":
                                if st.button("🔍 Ver detalles", key="btn_intra_stats", use_container_width=True):
                                    st.session_state['ver_subdimensiones_intra'] = True
                                    st.rerun()
                        # --- DENTRO DEL FOR NOMBRE, DF_G, COLUMNA EN DIMS_GLOBALES ---
                        with c2:
                            if st.button(f"📊 Analizar {nombre}", key=f"ai_analisis_{nombre}", use_container_width=True):
                                with st.spinner(f"Analizando datos de {nombre}..."):
                                    data_context = df_g_pct[['Nivel', 'Porcentaje']].to_string(index=False)
                                    
                                    prompt_analisis = (
                                        f"Analiza técnicamente los resultados de la dimensión '{nombre}'. "
                                        f"Datos: {data_context}. Identifica el riesgo predominante y su impacto."
                                    )
                                    
                                    config_analisis = config_ia.copy()
                                    config_analisis["formato"] = "Párrafos con negritas y subtítulos" # Mejoramos el formato
                                    
                                    respuesta = consultar_gemini(prompt_analisis, config_personalizada=config_analisis)
                                    
                                    # LLAMADA AL MODAL: En lugar de st.info(respuesta)
                                    mostrar_analisis_modal(nombre, respuesta)
                                    
                                    # Usamos st.success o st.info para mostrar el diagnóstico
                                    st.markdown(f"**🔍 Diagnóstico Estadístico - {nombre}:**")
                                    st.write(respuesta)

                st.markdown("---")
                st.subheader("🍩 Distribución y Volumen de Riesgos")

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
                    fig_dona.add_annotation(text=f"<span style='color:white; text-shadow: 2px 2px 4px #000000;'><b>{total_personas}</b><br>Encuestados</span>",
                                          showarrow=False, font=dict(size=22), x=0.5, y=0.5)
                    fig_dona.update_layout(showlegend=False, height=450, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_dona, use_container_width=True)

                with col_lista:
                    st.markdown("#### 📊 Conteo de Respuestas")
                    for _, row in df_consolidado.iterrows():
                        color = COLORES_RIESGO.get(row['Nivel'], "#333")
                        st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #333; margin-bottom: 5px; background: rgba(255,255,255,0.02); border-radius: 5px;">
                                <span style="border-left: 5px solid {color}; padding-left: 15px; color: #E0E0E0; font-size: 14px;">{row['Nivel']}</span>
                                <span style="background: {color}33; color: white; padding: 2px 12px; border-radius: 15px; font-weight: bold; border: 1px solid {color}; font-size: 14px;">{int(row['Valor'])}</span>
                            </div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div style="margin-top: 25px; padding: 20px; background: linear-gradient(135deg, #2c3e50 0%, #000000 100%); border-radius: 12px; border: 1px solid #444; text-align: center;">
                            <p style="margin:0; color: #aaa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Total Respuestas Analizadas</p>
                            <h1 style="margin:0; color: white; font-size: 42px; font-weight: 800;">{total_respuestas}</h1>
                        </div>""", unsafe_allow_html=True)
            
            else:
                # --- VISTA SUBDIMENSIONES ---
                st.markdown("### 🧱 Desglose: Subdimensiones Intralaborales (A+B)")
                
                # --- NUEVA SECCIÓN: TOP 3 CRÍTICOS ---
                try:
                    df_informe = pd.read_excel(archivo, sheet_name="Informe General", header=None, engine=motor)
                    
                    # 1. Definimos las coordenadas de todas las subdimensiones para analizarlas
                    analisis_sub = {
                        "Demandas emocionales": {"cols": range(2, 8), "row_header": 2, "row_data": 4},
                        "Demandas de jornada": {"cols": range(11, 16), "row_header": 2, "row_data": 4},
                        "Control sobre el trabajo": {"cols": range(20, 25), "row_header": 2, "row_data": 4}, # Ajusta según tu Excel
                        "Liderazgo": {"cols": range(29, 34), "row_header": 2, "row_data": 4} # Ajusta según tu Excel
                    }

                    ranking_critico = []

                    for nombre_sub, coords in analisis_sub.items():
                        try:
                            vals = pd.to_numeric(df_informe.iloc[coords['row_data'], coords['cols']], errors='coerce').fillna(0).tolist()
                            heads = df_informe.iloc[coords['row_header'], coords['cols']].tolist()
                            
                            # Calculamos el % crítico (Alto + Muy Alto)
                            crit_sum = 0
                            for h, v in zip(heads, vals):
                                if h in ["Riesgo alto", "Riesgo muy alto"]:
                                    crit_sum += (v * 100 if v <= 1.0 else v)
                            
                            ranking_critico.append({"Subdimensión": nombre_sub, "Crítico": crit_sum})
                        except: continue

                    # 2. Ordenamos y tomamos las 3 peores
                    top_3 = sorted(ranking_critico, key=lambda x: x['Crítico'], reverse=True)[:3]

                    # 3. Renderizamos las Mini-Tarjetas de Alerta
                    st.write("⚠️ **Dimensiones con mayor impacto negativo:**")
                    cols_top = st.columns(3)
                    for i, item in enumerate(top_3):
                        with cols_top[i]:
                            st.markdown(f"""
                                <div style="background: rgba(192, 57, 43, 0.1); border-left: 5px solid #C0392B; 
                                            padding: 15px; border-radius: 5px;">
                                    <p style="margin:0; font-size: 12px; color: #aaa;"># {i+1} Crítica</p>
                                    <h4 style="margin:5px 0; font-size: 14px; color: white;">{item['Subdimensión']}</h4>
                                    <h3 style="margin:0; color: #E74C3C;">{item['Crítico']:.1f}%</h3>
                                </div>
                            """, unsafe_allow_html=True)
                except:
                    st.warning("No se pudo generar el ranking automático.")

                st.markdown("---")
                
                if st.button("⬅️ Volver al Resumen Global"):
                    st.session_state['ver_subdimensiones_intra'] = False
                    st.rerun()
                
                try:
                    df_informe = pd.read_excel(archivo, sheet_name="Informe General", header=None)
                    
                    mapeo_manual = {
                        "Demandas emocionales": {"cols": range(2, 8), "row_header": 2, "row_data": 4},
                        "Demandas de jornada laboral": {"cols": range(11, 16), "row_header": 2, "row_data": 4}
                    }
                    
                    for sub, coords in mapeo_manual.items():
                        with st.expander(f"📌 {sub.upper()}", expanded=True):
                            try:
                                cabeceras = df_informe.iloc[coords['row_header'], coords['cols']].tolist()
                                valores = df_informe.iloc[coords['row_data'], coords['cols']].tolist()
                                
                                df_sub = pd.DataFrame({"Nivel": cabeceras, "Valor": valores})
                                df_sub = df_sub[df_sub["Nivel"] != "Total general"]
                                
                                df_sub['Valor'] = pd.to_numeric(df_sub['Valor'], errors='coerce').fillna(0)
                                if df_sub['Valor'].max() <= 1.0 and df_sub['Valor'].max() > 0:
                                    df_sub['Valor'] = df_sub['Valor'] * 100

                                c_info, c_chart = st.columns([1, 2])
                                
                                df_sub['Nivel'] = pd.Categorical(df_sub['Nivel'], categories=ORDEN_RIESGO, ordered=True)
                                df_sub = df_sub.sort_values('Nivel').dropna(subset=['Nivel'])
                                crit_val = df_sub[df_sub["Nivel"].isin(["Riesgo alto", "Riesgo muy alto"])]["Valor"].sum()
                                
                                with c_info:
                                    st.error(f"**Riesgo Crítico:** {crit_val:.1f}%")
                                    st.dataframe(df_sub, hide_index=True)
                                    # Botón IA para subdimensión
                                    if st.button(f"🪄 Plan IA: {sub}", key=f"ai_plan_sub_{sub}"):
                                        with st.spinner(f"Analizando {sub}..."):
                                            data_sub_ctx = df_sub[['Nivel', 'Valor']].to_string(index=False)
                                            st.info(consultar_gemini(prompt_usuario=f"Como experto en salud mental laboral, sugiere 2 estrategias para la subdimensión '{sub}' con estos datos: {data_sub_ctx}",config_personalizada=None, tokens=700))

                                with c_chart:
                                    fig_sub = px.bar(
                                        df_sub, 
                                        x='Valor', 
                                        y='Nivel', 
                                        orientation='h', 
                                        color='Nivel', 
                                        color_discrete_map=COLORES_RIESGO,
                                        text=df_sub['Valor'].apply(lambda x: f'{x:.1f}%' if x > 0 else '')
                                    )
                                    fig_sub.update_layout(
                                        xaxis_title="Porcentaje (%)",
                                        yaxis_title="",
                                        xaxis=dict(range=[0, 105]),
                                        showlegend=False,
                                        height=300
                                    )
                                    fig_sub.update_traces(textposition='outside')
                                    st.plotly_chart(fig_sub, use_container_width=True, key=f"chart_{sub}")
                            except Exception as inner_e:
                                st.warning(f"No se pudo extraer {sub}.")

                except Exception as e:
                    st.error(f"Error al procesar la hoja 'Informe General'.")

    except Exception as e:
        st.error(f"Error en procesamiento.")