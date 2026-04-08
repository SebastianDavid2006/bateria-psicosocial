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
    # AÑADE 'extraer_tabla_por_titulo' A ESTA LISTA 👇
    from utils.extractor import (
        extraer_datos_psicosocial, 
        procesar_dimensiones_por_grupo, 
        CONFIG_BATERIA,
        extraer_tabla_por_titulo  # <--- ESTA ES LA QUE FALTA
    )
    from utils.consultar_gemini import consultar_gemini
    from components.tabs_view import render_tabs
    from components.explorador import render_explorador_dinamico
    from utils.catalogo_acciones import obtener_diagnostico_completo
    from utils.estrategias import ESTRATEGIAS_MANUAL
except ModuleNotFoundError as e:
    st.error(f"❌ Error al cargar módulos internos: {e}")
    st.stop()

# Función para asignar colores a los tipos de acción
def obtener_color_tipo(tipo_accion):
    tipo = tipo_accion.lower()
    if "primaria" in tipo:
        return "#00b4d8"  # Azul claro (Educación / Prevención base)
    elif "secundaria" in tipo:
        return "#ffb703"  # Amarillo/Naranja (Alerta / Intervención focalizada)
    elif "terciaria" in tipo:
        return "#e63946"  # Rojo (Choque / Rehabilitación / Crisis)
    return "#8d99ae"      # Gris por defecto

@st.dialog("📊 Diagnóstico de Riesgo Psicosocial")
def mostrar_analisis_modal(titulo, contenido):
    st.write(f"### Análisis: {titulo}")
    
    # Contenedor con scroll por si la IA se extiende
    with st.container(height=400, border=False):
        st.markdown(contenido)
    
    if st.button("✅ Entendido", use_container_width=True):
        st.rerun()

@st.dialog("🎯 Plan de Acción Estratégico", width="large")
def mostrar_estrategias_modal(dimension, nivel, estrategias):
    st.markdown(f"### {dimension}")
    st.markdown(f"**Nivel de Riesgo detectado:** `{nivel}`")
    st.divider()
    
    if estrategias:
        for plan in estrategias:
            color_b = obtener_color_tipo(plan.get("tipo", ""))
            st.markdown(f"""
                <div class="strategy-card-modal" style="border-left-color: {color_b} !important;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="background: {color_b}; color: white; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">
                            {plan.get('tipo').upper()}
                        </span>
                        <span style="opacity: 0.6; font-size: 12px;">📍 {plan.get('responsable', 'RRHH')}</span>
                    </div>
                    <div style="font-size: 16px; color: #f0f2f6; line-height: 1.5; font-weight: 500;">
                        {plan.get('accion')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No se requieren acciones críticas según los parámetros actuales.")
    
    if st.button("Cerrar", use_container_width=True):
        st.rerun()

@st.dialog("📊 Análisis Ejecutivo para Líderes")
def mostrar_reporte_ia_modal(dimension, area, analisis):
    st.write(f"### Dimensión: {dimension}")
    st.caption(f"📍 Análisis personalizado para el área de **{area}**")
    st.divider()
    
    with st.container(height=350, border=False):
        st.markdown(analisis)
    
    if st.button("Cerrar", use_container_width=True):
        st.rerun()

# --- 3. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Batería Psicosocial AI", layout="wide")

# --- 4. CSS Y ESTILOS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            # ¡AQUÍ ESTABA EL ERROR! Faltaba el f.read() dentro de las etiquetas style
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llamada a la función (asegúrate de que la ruta sea correcta)
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
    "Sin Riesgo": "#43DF1C", 
    "Riesgo bajo": "#96FFE3", 
    "Riesgo medio": "#FFDC4F",
    "Riesgo alto": "#FF8A00", 
    "Riesgo muy alto": "#D33A34", 
    "Dato perdido": "#D3D3D3"
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
            # --- CONFIGURACIÓN IA POR DEFECTO ---
            config_ia = {
                "formato": "Lista de viñetas",
                "tono": "Profesional y Técnico",
                "max_palabras": 150
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
                # 1. Definición de Dominios y sus Dimensiones (Títulos exactos del Excel)
                DOMINIOS_MAP = {
                    "Liderazgo y Relaciones": [
                        "Caracteristicas Liderazgo", 
                        "Relaciones Sociales", 
                        "Retroal. Desempeño", 
                        "Relación colaboradores"
                    ],
                    "Control sobre el Trabajo": [
                        "Claridad de Rol",
                        "Capacitación",
                        "Participación y manejo del cambio",
                        "Oportunidades para el desarrollo",
                        "e Control y autonomia sobre el trabajo"
                    ],
                    "Demandas del Trabajo": [
                        "Demandas cuantitativas",
                        "Demandas emocionales",
                        "Demandas de carga mental",
                        "Demandas ambientales y de esfuerzo fisico",
                        "Demandas de jornada laboral",
                        "Exigencias de responsabilidad",
                        "Consistencia de rol",
                        "Influencia sobre el entorno extra"
                    ],
                    "Recompensas": [
                        "Reconocimiento y compensación",
                        "Recompensas de pertenencia y trabajo"
                    ]
                }

                st.markdown("### 🧱 Gestión por Dominios")
                
                col_back, col_area, col_dominio = st.columns([0.8, 1.6, 1.6])
                
                with col_back:
                    if st.button("⬅️ Volver", use_container_width=True):
                        st.session_state['ver_subdimensiones_intra'] = False
                        st.rerun()

                try:
                    # Carga de la hoja Informe General
                    extension_inf = archivo.name.split('.')[-1].lower()
                    motor_inf = "pyxlsb" if extension_inf == "xlsb" else None
                    df_informe = pd.read_excel(archivo, sheet_name="Informe General", header=None, engine=motor_inf)
                    
                    # --- DETECCIÓN DE ÁREAS ---
                    columna_areas = 13 
                    lista_areas_raw = df_informe.iloc[:, columna_areas].dropna().unique().tolist()
                    omitir = ["ETIQUETAS DE FILA", "(EN BLANCO)", "TOTAL GENERAL", "ÁREA", "VALORES"]
                    lista_areas = [str(a).strip() for a in lista_areas_raw if str(a).strip().upper() not in omitir and len(str(a)) > 2]
                    
                    with col_area:
                        area_sel = st.selectbox("📍 Seleccione Área:", sorted(lista_areas))
                    
                    with col_dominio:
                        dominio_sel = st.selectbox("📂 Dominio a Validar:", list(DOMINIOS_MAP.keys()))

                    st.markdown("---")
                    st.subheader(f"📊 Detalle: {dominio_sel}")

                    # --- BUCLE DINÁMICO DE DIMENSIONES ---
                    # Esto reemplaza los bloques 'especialistas' manuales
                    dimensiones_a_procesar = DOMINIOS_MAP[dominio_sel]
                    
                    # Creamos una rejilla de 2 columnas para las gráficas
                    grid_cols = st.columns(2)
                    
                    for idx, nombre_dimension in enumerate(dimensiones_a_procesar):
                        # --- DENTRO DEL BUCLE DE DIMENSIONES ---
                        with grid_cols[idx % 2]:
                            # 1. Extraer los datos primero
                            df_dim = extraer_tabla_por_titulo(df_informe, nombre_dimension, area_sel)
                            
                            if not df_dim.empty and "Valor" in df_dim.columns:
                                # 2. INICIALIZAR VARIABLES (Evita el error 'not defined')
                                emoji = "📊" 
                                clase_tarjeta = "bg-normal"
                                label_texto = "RIESGO CONTROLADO"
                                nivel_key = "Sin Riesgo"
                                
                                # 3. CÁLCULOS DE RIESGO
                                val_alto = df_dim[df_dim["Nivel"] == "Riesgo alto"]["Valor"].sum()
                                val_muy_alto = df_dim[df_dim["Nivel"] == "Riesgo muy alto"]["Valor"].sum()
                                riesgo_total_critico = val_alto + val_muy_alto

                                # 4. LÓGICA DE CATEGORIZACIÓN (Asignación de variables para el visual)
                                if riesgo_total_critico >= 85.0:
                                    clase_tarjeta, emoji, label_texto, nivel_key = "bg-muy-alto", "🛑", "RIESGO MUY ALTO", "Muy Alto"
                                elif riesgo_total_critico >= 70.0:
                                    clase_tarjeta, emoji, label_texto, nivel_key = "bg-alto", "⚠️", "RIESGO ALTO", "Alto"
                                elif riesgo_total_critico >= 50.0:
                                    clase_tarjeta, emoji, label_texto, nivel_key = "bg-medio", "🔸", "RIESGO MEDIO", "Medio"
                                elif riesgo_total_critico >= 10.0:
                                    clase_tarjeta, emoji, label_texto, nivel_key = "bg-bajo", "🔹", "RIESGO BAJO", "Bajo"

                                # 5. GENERAR GRÁFICA (La creamos antes de mostrarla)
                                fig = px.bar(df_dim, x='Valor', y='Nivel', orientation='h',
                                            color='Nivel', color_discrete_map=COLORES_RIESGO,
                                            text=df_dim['Valor'].apply(lambda x: f'{x:.1f}%'))

                                fig.update_layout(
                                    height=220, showlegend=False, margin=dict(t=5, b=5, l=0, r=50),
                                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    xaxis_visible=False, yaxis_title="",
                                    yaxis={'categoryorder':'array', 'categoryarray': ORDEN_RIESGO[::-1]}
                                )
                                fig.update_traces(textposition='outside', marker_line_width=0)

                                # 6. RENDERIZADO VISUAL (Ahora que todo está definido)
                                with st.expander(f"{emoji} {nombre_dimension.upper()}", expanded=True):
                                    # Cabecera: Métrica + Botón Popover
                                    col_metrica, col_accion = st.columns([3, 1.2])
                                    
                                    with col_metrica:
                                        st.markdown(f"""
                                            <div class="risk-card {clase_tarjeta}">
                                                <div class="label">{label_texto}</div>
                                                <div class="value">{riesgo_total_critico:.1f}%</div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                        with col_accion:
                                            # --- BOTÓN 1: REPORTE IA ---
                                            if st.button("📊 Reporte IA", key=f"ai_rep_{idx}", use_container_width=True):
                                                with st.spinner("🤖 Gemini analizando impacto..."):
                                                    datos_tabla = df_dim[['Nivel', 'Valor']].to_string(index=False)
                                                    prompt = f"""
                                                    Actúa como consultor senior. 
                                                    Explica al jefe del área de {area_sel} el impacto operativo de estos 
                                                    resultados en la dimensión {nombre_dimension}:
                                                    {datos_tabla}
                                                    Sé breve, usa viñetas y enfócate en productividad y clima.
                                                    """
                                                    respuesta = consultar_gemini(prompt)
                                                    mostrar_reporte_ia_modal(nombre_dimension, area_sel, respuesta)

                                            # Espacio entre botones
                                            st.write("") 

                                            # --- BOTÓN 2: VER PLAN ---
                                            # Obtenemos la lista pero NO la recorremos aquí con un 'for'
                                            lista_planes = ESTRATEGIAS_MANUAL.get(nombre_dimension, {}).get(nivel_key, [])
                                            
                                            if st.button("🚀 Ver Plan", key=f"btn_plan_{idx}", use_container_width=True, type="primary"):
                                                mostrar_estrategias_modal(nombre_dimension, nivel_key, lista_planes)

                                    # Gráfica principal
                                    st.plotly_chart(fig, use_container_width=True, key=f"chart_modern_{idx}")
                            else:
                                st.error(f"❌ No se encontró la tabla o está vacía: '{nombre_dimension}'")

                except Exception as e:
                    st.error(f"⚠️ Error en la vista de dominios: {e}")
                    # Opcional: imprimir el error en consola para debug
                    print(f"Error detallado: {e}")

    except Exception as e:
        st.error(f"Error en procesamiento.")