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

def crear_html_seccion(titulo, contenido):
    numeros = {"OBJETIVO": "1", "BENEFICIOS": "2", "CONSIDERACIONES": "3"}
    colores = {
        "OBJETIVO": ("linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "#667eea"),
        "BENEFICIOS": ("linear-gradient(135deg, #11998e 0%, #38ef7d 100%)", "#11998e"),
        "CONSIDERACIONES": ("linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "#f093fb")
    }
    num = numeros.get(titulo, "?")
    gradiente, color_solido = colores.get(titulo, (colores["OBJETIVO"]))
    
    return f"""
    <div style="display: flex; gap: 10px; align-items: stretch; margin-bottom: 5px;">
        <div style="background: {gradiente}; width: 50px; min-height: 60px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white; flex-shrink: 0;">{num}</div>
        <div style="background: #1e1e2e; border-radius: 10px; padding: 10px 15px; flex-grow: 1; border-left: 3px solid {color_solido};">
            <div style="font-size: 12px; color: #888; margin-bottom: 5px; text-transform: uppercase;">{titulo}</div>
            <div style="color: #e0e0e0; font-size: 14px;">{contenido}</div>
        </div>
    </div>
    """

@st.dialog("📊 Análisis de Estrategia", width="large")
def mostrar_analisis_estrategia(dimension, estrategia, tipo):
    st.markdown(f"### {estrategia}")
    st.markdown(f"**Tipo:** `{tipo}`")
    st.divider()
    
    with st.spinner("Generando análisis con IA..."):
        prompt = f"""
        Para la estrategia de prevención de riesgos psicosociales:
        
        Estrategia: {estrategia}
        Tipo: {tipo}
        Dimensión: {dimension}
        
        Proporciona:
        1. OBJETIVO: ¿Qué busca lograr esta estrategia?
        2. BENEFICIOS: ¿Qué beneficios trae a la organización y trabajadores?
        3. CONSIDERACIONES: ¿Qué aspectos importantes deben considerarse para su implementación?
        
        Sé breve y concreto.
        """
        respuesta = consultar_gemini(prompt)
    
    partes = respuesta.split("\n\n")
    for parte in partes:
        if parte.strip().upper().startswith("OBJETIVO"):
            contenido = parte.replace("OBJETIVO:", "").strip()
            st.markdown(crear_html_seccion("OBJETIVO", contenido), unsafe_allow_html=True)
        elif parte.strip().upper().startswith("BENEFICIO"):
            contenido = parte.replace("BENEFICIOS:", "").replace("BENEFICIO:", "").strip()
            st.markdown(crear_html_seccion("BENEFICIOS", contenido), unsafe_allow_html=True)
        elif parte.strip().upper().startswith("CONSIDERAC"):
            contenido = parte.replace("CONSIDERACIONES:", "").strip()
            st.markdown(crear_html_seccion("CONSIDERACIONES", contenido), unsafe_allow_html=True)
    
    if st.button("Cerrar", use_container_width=True):
        st.rerun()

@st.dialog("🎯 Plan de Acción Estratégico", width="large")
def mostrar_estrategias_modal(dimension, nivel, estrategias):
    st.markdown(f"### {dimension}")
    st.markdown(f"**Nivel de Riesgo detectado:** `{nivel}`")
    st.divider()
    
    if estrategias:
        for idx, plan in enumerate(estrategias):
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
            
            # Usamos expander en lugar de dialog anidado
            with st.expander("✨ Analizar con IA"):
                with st.spinner("Generando análisis..."):
                    prompt = f"""
                    Para la estrategia de prevención de riesgos psicosociales:
                    
                    Estrategia: {plan.get('accion')}
                    Tipo: {plan.get('tipo')}
                    Dimensión: {dimension}
                    
                    Proporciona:
                    1. OBJETIVO: ¿Qué busca lograr esta estrategia?
                    2. BENEFICIOS: ¿Qué beneficios trae a la organización y trabajadores?
                    3. CONSIDERACIONES: ¿Qué aspectos importantes deben considerarse para su implementación?
                    
                    Sé breve y concreto.
                    """
                    respuesta = consultar_gemini(prompt)
                
                partes = respuesta.split("\n\n")
                for parte in partes:
                    if parte.strip().upper().startswith("OBJETIVO"):
                        contenido = parte.replace("OBJETIVO:", "").strip()
                        st.markdown(crear_html_seccion("OBJETIVO", contenido), unsafe_allow_html=True)
                    elif parte.strip().upper().startswith("BENEFICIO"):
                        contenido = parte.replace("BENEFICIOS:", "").replace("BENEFICIO:", "").strip()
                        st.markdown(crear_html_seccion("BENEFICIOS", contenido), unsafe_allow_html=True)
                    elif parte.strip().upper().startswith("CONSIDERAC"):
                        contenido = parte.replace("CONSIDERACIONES:", "").strip()
                        st.markdown(crear_html_seccion("CONSIDERACIONES", contenido), unsafe_allow_html=True)
            
            st.write("")
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

                    # --- TOP 3 ÁREAS CON MAYOR RIESGO (GLOBAL) - Solo se calcula una vez ---
                    cache_key = "riesgos_areas_cache"
                    if cache_key not in st.session_state:
                        @st.cache_data(ttl=3600)
                        def calcular_riesgos_todas_areas(lista_areas, df_informe):
                            riesgos = []
                            
                            # Solo dimensiones de Intralaboral
                            dims_intra = ["Caracteristicas Liderazgo", "Relaciones Sociales", "Retroal. Desempeño", "Relación colaboradores", 
                                "Claridad de Rol", "Capacitación", "Participación y manejo del cambio", "Oportunidades para el desarrollo", 
                                "e Control y autonomia sobre el trabajo", "Demandas cuantitativas", "Demandas emocionales", 
                                "Demandas de carga mental", "Demandas ambientales y de esfuerzo fisico", "Demandas de jornada laboral",
                                "Exigencias de responsabilidad", "Consistencia de rol", "Influencia sobre el entorno extra"]
                            
                            for area in lista_areas:
                                riesgo_total = 0
                                count_dims = 0
                                for dim in dims_intra:
                                    try:
                                        df_dim = extraer_tabla_por_titulo(df_informe, dim, area)
                                        if not df_dim.empty and "Valor" in df_dim.columns:
                                            val_alto = df_dim[df_dim["Nivel"] == "Riesgo alto"]["Valor"].sum()
                                            val_muy_alto = df_dim[df_dim["Nivel"] == "Riesgo muy alto"]["Valor"].sum()
                                            riesgo_total += val_alto + val_muy_alto
                                            count_dims += 1
                                    except:
                                        continue
                                
                                riesgo_promedio = riesgo_total / count_dims if count_dims > 0 else 0
                                
                                # Clasificación según nuevos rangos
                                if riesgo_promedio >= 85:
                                    nivel = "Riesgo Muy Alto"
                                    color = "#D33A34"
                                elif riesgo_promedio >= 70:
                                    nivel = "Riesgo Alto"
                                    color = "#FF8A00"
                                elif riesgo_promedio >= 50:
                                    nivel = "Riesgo Medio"
                                    color = "#FFDC4F"
                                elif riesgo_promedio >= 30:
                                    nivel = "Riesgo Bajo"
                                    color = "#96FFE3"
                                else:
                                    nivel = "Sin Riesgo"
                                    color = "#4CAF50"
                                
                                riesgos.append((area, riesgo_promedio, nivel, color))
                            
                            return sorted(riesgos, key=lambda x: x[1], reverse=True)

                        st.session_state[cache_key] = calcular_riesgos_todas_areas(lista_areas, df_informe)
                    
                    riesgos_todas = st.session_state[cache_key]
                    
                    if riesgos_todas and riesgos_todas[0][1] > 0:
                        st.write("")
                        # Fila título + botón (botón debajo pero alineado a la derecha)
                        st.markdown('<p style="font-size: 16px; font-weight: 600; margin: 0;">Áreas con Mayor Riesgo</p>', unsafe_allow_html=True)
                        
                        with st.container():
                            col_btn = st.columns([1])
                            with col_btn[0]:
                                if st.button("📊 Ver más", key="btn_ver_todas", use_container_width=False):
                                    st.session_state['mostrar_todas_areas'] = True
                        
                        cols_areas = st.columns(3)
                        for i in range(min(3, len(riesgos_todas))):
                            area, riesgo, nivel, color = riesgos_todas[i]
                            with cols_areas[i]:
                                if "Muy Alto" in nivel:
                                    gradiente = "linear-gradient(145deg, #c0392b 0%, #8e2a1f 50%, #5c1914 100%)"
                                    borde = "#e74c3c"
                                elif "Alto" in nivel:
                                    gradiente = "linear-gradient(145deg, #d35400 0%, #a04000 50%, #6e2c00 100%)"
                                    borde = "#e67e22"
                                elif "Medio" in nivel:
                                    gradiente = "linear-gradient(145deg, #f39c12 0%, #d68910 50%, #b9770e 100%)"
                                    borde = "#f1c40f"
                                elif "Bajo" in nivel:
                                    gradiente = "linear-gradient(145deg, #27ae60 0%, #1e8449 50%, #145a32 100%)"
                                    borde = "#2ecc71"
                                else:
                                    gradiente = "linear-gradient(145deg, #1abc9c 0%, #16a085 50%, #117a65 100%)"
                                    borde = "#1abc9c"
                                
                                st.markdown(f"""<div style="background: {gradiente}; border-radius: 15px; padding: 20px; border: 2px solid {borde}; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);">
                                    <div style="font-size: 26px; font-weight: bold; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{int(riesgo)}%</div>
                                    <div style="font-size: 14px; color: white; font-weight: 600; margin-top: 8px;">{area}</div>
                                    <div style="font-size: 11px; color: rgba(255,255,255,0.85); margin-top: 5px; font-weight: 500;">{nivel}</div>
                                </div>""", unsafe_allow_html=True)
                        st.write("")
                        
                        if 'mostrar_todas_areas' not in st.session_state:
                            st.session_state['mostrar_todas_areas'] = False
                        
                        if st.session_state['mostrar_todas_areas'] and riesgos_todas:
                            @st.dialog("Todas las Áreas por Nivel de Riesgo")
                            def mostrar_todas_areas_modal():    
                                
                                # Contenedor con márgenes internos
                                with st.container(height=450, border=False):
                                    for area, riesgo, nivel, color in riesgos_todas:
                                        if "Muy Alto" in nivel:
                                            gradiente = "linear-gradient(145deg, #c0392b 0%, #8e2a1f 50%, #5c1914 100%)"
                                            borde = "#e74c3c"
                                        elif "Alto" in nivel:
                                            gradiente = "linear-gradient(145deg, #d35400 0%, #a04000 50%, #6e2c00 100%)"
                                            borde = "#e67e22"
                                        elif "Medio" in nivel:
                                            gradiente = "linear-gradient(145deg, #f39c12 0%, #d68910 50%, #b9770e 100%)"
                                            borde = "#f1c40f"
                                        elif "Bajo" in nivel:
                                            gradiente = "linear-gradient(145deg, #27ae60 0%, #1e8449 50%, #145a32 100%)"
                                            borde = "#2ecc71"
                                        else:
                                            gradiente = "linear-gradient(145deg, #1abc9c 0%, #16a085 50%, #117a65 100%)"
                                            borde = "#1abc9c"
                                        
                                        st.markdown(f"""<div style="background: {gradiente}; border-radius: 12px; padding: 16px; border: 2px solid {borde}; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                                            <div style="font-size: 15px; color: white; font-weight: 600;">{area}</div>
                                            <div style="text-align: right;">
                                                <div style="font-size: 22px; font-weight: bold; color: white;">{int(riesgo)}%</div>
                                                <div style="font-size: 10px; color: rgba(255,255,255,0.85);">{nivel}</div>
                                            </div>
                                        </div>""", unsafe_allow_html=True)
                                
                                st.write("")
                                if st.button("Cerrar", use_container_width=True):
                                    st.session_state['mostrar_todas_areas'] = False
                                    st.rerun()
                            
                            mostrar_todas_areas_modal()

                    # --- TOP 3 DIMENSIONES CON MAYOR RIESGO (GENERAL) - Cache por área ---
                    cache_key_dimensiones = f"riesgos_dimensiones_{area_sel}"
                    if cache_key_dimensiones not in st.session_state:
                        todos_riesgos = []
                        for dominio in DOMINIOS_MAP.keys():
                            for nombre_dimension in DOMINIOS_MAP[dominio]:
                                df_dim = extraer_tabla_por_titulo(df_informe, nombre_dimension, area_sel)
                                if not df_dim.empty and "Valor" in df_dim.columns:
                                    val_alto = df_dim[df_dim["Nivel"] == "Riesgo alto"]["Valor"].sum()
                                    val_muy_alto = df_dim[df_dim["Nivel"] == "Riesgo muy alto"]["Valor"].sum()
                                    riesgo_critico = val_alto + val_muy_alto
                                    todos_riesgos.append((nombre_dimension, riesgo_critico, dominio))
                        
                        todos_riesgos.sort(key=lambda x: x[1], reverse=True)
                        st.session_state[cache_key_dimensiones] = todos_riesgos
                    
                    todos_riesgos = st.session_state[cache_key_dimensiones]
                    
                    if todos_riesgos and todos_riesgos[0][1] > 0:
                        st.write("")
                        # Título + botón
                        st.markdown('<p style="font-size: 16px; font-weight: 600; margin: 0;">Dimensiones con Mayor Riesgo General</p>', unsafe_allow_html=True)
                        
                        with st.container():
                            col_btn = st.columns([1])
                            with col_btn[0]:
                                if st.button("📊 Ver más", key="btn_ver_todas_dim_gen", use_container_width=False):
                                    st.session_state['mostrar_todas_dimensiones'] = True
                        
                        cols_top = st.columns(3)
                        for i in range(min(3, len(todos_riesgos))):
                            dim, riesgo, dom = todos_riesgos[i]
                            with cols_top[i]:
                                if riesgo >= 85:
                                    gradiente = "linear-gradient(135deg, #8B0000 0%, #5c0000 100%)"
                                    borde = "#ff4444"
                                    nivel_texto = "Riesgo Muy Alto"
                                    color_letra = "white"
                                    color_sub = "#ddd"
                                elif riesgo >= 70:
                                    gradiente = "linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%)"
                                    borde = "#ff4444"
                                    nivel_texto = "Riesgo Alto"
                                    color_letra = borde
                                    color_sub = borde
                                elif riesgo >= 50:
                                    gradiente = "linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%)"
                                    borde = "#e67e22"
                                    nivel_texto = "Riesgo Medio"
                                    color_letra = borde
                                    color_sub = borde
                                elif riesgo >= 30:
                                    gradiente = "linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%)"
                                    borde = "#2ecc71"
                                    nivel_texto = "Riesgo Bajo"
                                    color_letra = borde
                                    color_sub = borde
                                else:
                                    gradiente = "linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%)"
                                    borde = "#27ae60"
                                    nivel_texto = "Sin Riesgo"
                                    color_letra = borde
                                    color_sub = borde
                                
                                st.markdown(f"""<div style="background: {gradiente}; border-radius: 15px; padding: 18px; border: 2px solid {borde}; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
                                    <div style="font-size: 12px; color: {color_sub}; text-transform: uppercase; margin-bottom: 5px;">{dim}</div>
                                    <div style="font-size: 32px; font-weight: bold; color: {color_letra};">{int(riesgo)}%</div>
                                    <div style="font-size: 11px; color: {color_sub}; margin-top: 5px;">{nivel_texto} | {dom}</div>
                                </div>""", unsafe_allow_html=True)

                    st.write("")
                    
                    # Modal para todas las dimensiones (General)
                    if st.session_state.get('mostrar_todas_dimensiones', False) and todos_riesgos:
                        @st.dialog("Todas las Dimensiones por Nivel de Riesgo")
                        def mostrar_todas_dimensiones_modal():
                            
                            with st.container(height=450, border=False):
                                for dim, riesgo, dom in todos_riesgos:
                                    if riesgo >= 85:
                                        gradiente = "linear-gradient(145deg, #c0392b 0%, #8e2a1f 50%, #5c1914 100%)"
                                        borde = "#e74c3c"
                                        nivel_texto = "Riesgo Muy Alto"
                                    elif riesgo >= 70:
                                        gradiente = "linear-gradient(145deg, #d35400 0%, #a04000 50%, #6e2c00 100%)"
                                        borde = "#e67e22"
                                        nivel_texto = "Riesgo Alto"
                                    elif riesgo >= 50:
                                        gradiente = "linear-gradient(145deg, #f39c12 0%, #d68910 50%, #b9770e 100%)"
                                        borde = "#f1c40f"
                                        nivel_texto = "Riesgo Medio"
                                    elif riesgo >= 30:
                                        gradiente = "linear-gradient(145deg, #27ae60 0%, #1e8449 50%, #145a32 100%)"
                                        borde = "#2ecc71"
                                        nivel_texto = "Riesgo Bajo"
                                    else:
                                        gradiente = "linear-gradient(145deg, #1abc9c 0%, #16a085 50%, #117a65 100%)"
                                        borde = "#1abc9c"
                                        nivel_texto = "Sin Riesgo"
                                    
                                    st.markdown(f"""<div style="background: {gradiente}; border-radius: 12px; padding: 16px; border: 2px solid {borde}; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                                        <div style="font-size: 15px; color: white; font-weight: 600;">{dim}</div>
                                        <div style="text-align: right;">
                                            <div style="font-size: 22px; font-weight: bold; color: white;">{int(riesgo)}%</div>
                                            <div style="font-size: 10px; color: rgba(255,255,255,0.85);">{nivel_texto}</div>
                                        </div>
                                    </div>""", unsafe_allow_html=True)
                            
                            st.write("")
                            if st.button("Cerrar", use_container_width=True):
                                st.session_state['mostrar_todas_dimensiones'] = False
                                st.rerun()
                        
                        mostrar_todas_dimensiones_modal()
                    
                    # --- TOP 4 DIMENSIONES CON MAYOR RIESGO (DEL DOMINIO) - Cache por área y dominio ---
                    dimensiones_a_procesar = DOMINIOS_MAP[dominio_sel]
                    
                    cache_key_domain = f"riesgos_dominio_{area_sel}_{dominio_sel}"
                    if cache_key_domain not in st.session_state:
                        riesgos_dim = []
                        for nombre_dimension in dimensiones_a_procesar:
                            df_dim = extraer_tabla_por_titulo(df_informe, nombre_dimension, area_sel)
                            if not df_dim.empty and "Valor" in df_dim.columns:
                                val_alto = df_dim[df_dim["Nivel"] == "Riesgo alto"]["Valor"].sum()
                                val_muy_alto = df_dim[df_dim["Nivel"] == "Riesgo muy alto"]["Valor"].sum()
                                riesgo_critico = val_alto + val_muy_alto
                                riesgos_dim.append((nombre_dimension, riesgo_critico))
                        
                        riesgos_dim.sort(key=lambda x: x[1], reverse=True)
                        st.session_state[cache_key_domain] = riesgos_dim
                    
                    riesgos_dim = st.session_state[cache_key_domain]
                    
                    if riesgos_dim and riesgos_dim[0][1] > 0:
                        st.write("")
                        # Título + botón
                        st.markdown('<p style="font-size: 16px; font-weight: 600; margin: 0;">Dimensiones con Mayor Riesgo en este Dominio</p>', unsafe_allow_html=True)
                        
                        with st.container():
                            col_btn = st.columns([1])
                            with col_btn[0]:
                                if st.button("📊 Ver más", key="btn_ver_todas_dim_dom", use_container_width=False):
                                    st.session_state['mostrar_todas_dominio'] = True
                        
                        cols_criticas = st.columns(min(4, len(riesgos_dim)))
                        for i, (dim, riesgo) in enumerate(riesgos_dim[:4]):
                            if riesgo > 0:
                                with cols_criticas[i % min(4, len(riesgos_dim))]:
                                    if riesgo >= 85:
                                        color = "#D33A34"
                                    elif riesgo >= 70:
                                        color = "#FF8A00"
                                    elif riesgo >= 50:
                                        color = "#FFDC4F"
                                    elif riesgo >= 30:
                                        color = "#27ae60"
                                    else:
                                        color = "#66CDAA"
                                    st.markdown(f"""<div style="background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%); border-radius: 10px; padding: 12px; border-left: 4px solid {color}; margin-bottom: 10px;">
                                        <div style="font-size: 11px; color: #888; text-transform: uppercase;">{dim.upper()}</div>
                                        <div style="font-size: 24px; font-weight: bold; color: {color};">{int(riesgo)}%</div>
                                        <div style="font-size: 10px; color: #666;">Riesgo crítico</div>
                                    </div>""", unsafe_allow_html=True)
                        
                        st.divider()

                    # Modal para todas las dimensiones del dominio
                    if st.session_state.get('mostrar_todas_dominio', False) and riesgos_dim:
                        @st.dialog("Todas las Dimensiones del Dominio")
                        def mostrar_todas_dominio_modal():
                            st.markdown(f"### {dominio_sel}")
                            
                            with st.container(height=450, border=False):
                                for dim, riesgo in riesgos_dim:
                                    if riesgo >= 85:
                                        gradiente = "linear-gradient(145deg, #c0392b 0%, #8e2a1f 50%, #5c1914 100%)"
                                        borde = "#e74c3c"
                                        nivel_texto = "Riesgo Muy Alto"
                                    elif riesgo >= 70:
                                        gradiente = "linear-gradient(145deg, #d35400 0%, #a04000 50%, #6e2c00 100%)"
                                        borde = "#e67e22"
                                        nivel_texto = "Riesgo Alto"
                                    elif riesgo >= 50:
                                        gradiente = "linear-gradient(145deg, #f39c12 0%, #d68910 50%, #b9770e 100%)"
                                        borde = "#f1c40f"
                                        nivel_texto = "Riesgo Medio"
                                    elif riesgo >= 30:
                                        gradiente = "linear-gradient(145deg, #27ae60 0%, #1e8449 50%, #145a32 100%)"
                                        borde = "#2ecc71"
                                        nivel_texto = "Riesgo Bajo"
                                    else:
                                        gradiente = "linear-gradient(145deg, #1abc9c 0%, #16a085 50%, #117a65 100%)"
                                        borde = "#1abc9c"
                                        nivel_texto = "Sin Riesgo"
                                    
                                    st.markdown(f"""<div style="background: {gradiente}; border-radius: 12px; padding: 16px; border: 2px solid {borde}; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                                        <div style="font-size: 15px; color: white; font-weight: 600;">{dim}</div>
                                        <div style="text-align: right;">
                                            <div style="font-size: 22px; font-weight: bold; color: white;">{int(riesgo)}%</div>
                                            <div style="font-size: 10px; color: rgba(255,255,255,0.85);">{nivel_texto}</div>
                                        </div>
                                    </div>""", unsafe_allow_html=True)
                            
                            st.write("")
                            if st.button("Cerrar", use_container_width=True):
                                st.session_state['mostrar_todas_dominio'] = False
                                st.rerun()
                        
                        mostrar_todas_dominio_modal()

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
                                elif riesgo_total_critico >= 30.0:
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