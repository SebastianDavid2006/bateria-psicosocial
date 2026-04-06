import pandas as pd
import unicodedata
import re

CONFIG_BATERIA = {
    "INTRALABORAL": [
        #Liderazgo y Relaciones
        "Caracteristicas Liderazgo", 
        "Relaciones Sociales", 
        "Retroal. Desempeño", 
        "Relación colaboradores",
        #Control sobre el Trabajo
        "e Control y autonomia sobre el trabajo", 
        "Oportunidades para el desarrollo", 
        "Participación y manejo del cambIo", 
        "Claridad de rol", 
        "Capacitación",
        #Demandas del Trabajo
        "Demandas del Trabajo",
        "Demandas cuantitativas", 
        "Demandas de carga mental", 
        "Demandas emocionales", 
        "Exigencias de responsabilidad", 
        "Demandas ambientales y de esfuerzo fisico", 
        "Demandas de jornada laboral", 
        "Consistencia de rol", 
        "Influencia sobre el entorno extra",
        #Recompensas
        "Reconocimiento y compensación", 
        "Recompensas de pertenencia y trabajo"
    ]
}

ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]

def normalizar(texto):
    if not texto or pd.isna(texto): return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto).strip().upper())
                  if unicodedata.category(c) != 'Mn')

def buscar_coordenadas(df, texto_buscado):
    """Busca el título en todo el DataFrame y devuelve (fila, columna)."""
    texto_norm = normalizar(texto_buscado)
    for r in range(min(100, df.shape[0])): 
        for c in range(df.shape[1]):
            if texto_norm in normalizar(df.iloc[r, c]):
                return r, c
    return -1, -1

def extraer_bloque_principal(df, titulo_tabla):
    fila_t, col_t = buscar_coordenadas(df, titulo_tabla)
    if fila_t == -1:
        return pd.DataFrame({"Nivel": ORDEN_RIESGO, "Valor": [0.0]*6})

    datos = []
    es_estres = "ESTRÉS" in titulo_tabla.upper()
    
    if es_estres:
        etiquetas_orden_excel = ["Riesgo muy bajo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto", "Dato perdido"]
        SALTO_FILAS = 2 
    else:
        etiquetas_orden_excel = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto", "Dato perdido"]
        SALTO_FILAS = 1

    for i, etiqueta in enumerate(etiquetas_orden_excel):
        try:
            val = df.iloc[fila_t + SALTO_FILAS + i, col_t]
            if pd.isna(val) or str(val).strip() == "" or str(val).strip().lower() == "nan":
                val = 0.0
            else:
                val = float(str(val).replace(',', '.'))
        except:
            val = 0.0
        datos.append({"Nivel": etiqueta, "Valor": val})

    df_res = pd.DataFrame(datos)
    if es_estres:
        df_res["Nivel"] = df_res["Nivel"].replace("Riesgo muy bajo", "Sin Riesgo")

    return df_res.set_index("Nivel").reindex(ORDEN_RIESGO).reset_index().fillna(0)

def extraer_datos_psicosocial(df_raw, forma):
    return {
        "INTRALABORAL": extraer_bloque_principal(df_raw, f"Intralaboral {forma}"),
        "EXTRALABORAL": extraer_bloque_principal(df_raw, f"Extralaboral {forma}"),
        "ESTRÉS": extraer_bloque_principal(df_raw, f"Estrés {forma}")
    }

def extraer_subdimension(df_raw, nombre_sub):
    return extraer_bloque_principal(df_raw, nombre_sub)

# --- FUNCIÓN CORREGIDA PARA EL INFORME GENERAL (TABLA DINÁMICA) ---

def extraer_dimension_informe_general(df, dimension_nombre, area_objetivo):
    def norm(t):
        if pd.isna(t): return ""
        s = "".join(c for c in unicodedata.normalize('NFD', str(t)) if unicodedata.category(c) != 'Mn')
        return re.sub(r'[^A-Z0-9]', '', s.upper())

    niveles = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto"]
    res_vacio = pd.DataFrame({"Nivel": niveles, "Valor": [0.0] * 5})
    
    t_dim = norm(dimension_nombre)
    t_area = norm(area_objetivo)

    try:
        matriz = df.values.astype(str)
        f_dim, c_dim = -1, -1
        
        # 1. BUSCAR TÍTULO (Usamos 'in' para que 'Relaciones Sociales' pesque el nombre largo)
        for r in range(len(matriz)):
            for c in range(len(matriz[r])):
                if t_dim in norm(matriz[r, c]):
                    f_dim, c_dim = r, c
                    break
            if f_dim != -1: break

        if f_dim == -1: return res_vacio

        # 2. BUSCAR ÁREA
        f_area = -1
        limit = min(f_dim + 150, len(matriz))
        for r in range(f_dim, limit):
            fila_inicio = [norm(celda) for celda in matriz[r][:15]]
            if t_area in fila_inicio:
                f_area = r
                break

        # 3. EXTRAER VALORES
        if f_area != -1:
            numeros = []
            fila_datos = matriz[f_area]
            # Escaneamos desde la columna del título hacia la derecha
            for c in range(c_dim, min(c_dim + 20, len(fila_datos))):
                item = fila_datos[c].replace('%', '').replace(',', '.')
                m = re.search(r"(\d+\.?\d*)", item)
                if m:
                    n = float(m.group(1))
                    if 0 < n <= 1.05: n = n * 100
                    numeros.append(round(n, 2))

            # --- MAPEO CRÍTICO (Basado en tu Excel Dinámico) ---
            # Tu Excel suele botar: [Blanco, Bajo, Sin, Medio, Muy Alto, Alto, Total]
            # Si hay 6 o 7 números, el orden correcto para que cuadre con tu App es:
            if len(numeros) >= 6:
                # Quitamos el total si es > 99
                n_limpios = numeros[:-1] if numeros[-1] > 99.8 else numeros
                # Si el primero es el 'blanco' (0.0), lo ignoramos para alinear
                if n_limpios[0] < 0.01 and len(n_limpios) > 5:
                    n_limpios = n_limpios[1:]

                # Ahora asignamos según lo que vimos que funcionaba:
                return pd.DataFrame({
                    "Nivel": niveles,
                    "Valor": [
                        n_limpios[1], # Sin Riesgo
                        n_limpios[0], # Riesgo bajo
                        n_limpios[2], # Riesgo medio
                        n_limpios[4], # Riesgo alto
                        n_limpios[3]  # Riesgo muy alto
                    ]
                })

    except Exception as e:
        print(f"Error en {dimension_nombre}: {e}")

    return res_vacio

def procesar_dimensiones_por_grupo(df, grupo, area_objetivo):
    """
    Recorre la lista de dimensiones de un grupo y extrae los datos de cada una.
    Retorna un diccionario: { 'Nombre Dimension': DataFrame_con_5_niveles }
    """
    dict_resultados = {}
    
    # Obtenemos la lista de dimensiones para el grupo (ej. INTRALABORAL)
    dimensiones = CONFIG_BATERIA.get(grupo, [])
    
    for dim in dimensiones:
        # Llamamos a la función "Láser" que ya perfeccionamos
        df_res = extraer_dimension_informe_general(df, dim, area_objetivo)
        dict_resultados[dim] = df_res
        
    return dict_resultados

def obtener_top_riesgos(dict_resultados, top_n=3):
    resumen = []
    for nombre, df in dict_resultados.items():
        try:
            # Extraemos los valores buscando por el nombre de la fila
            alto = df.loc[df['Nivel'] == 'Riesgo alto', 'Valor'].values[0]
            muy_alto = df.loc[df['Nivel'] == 'Riesgo muy alto', 'Valor'].values[0]
            resumen.append({"Dimensión": nombre, "Suma": round(alto + muy_alto, 1)})
        except:
            continue
    return sorted(resumen, key=lambda x: x['Suma'], reverse=True)[:top_n]

def calcular_estadistica_dominio(resultados_intra, lista_dimensiones):
    """Saca el promedio de los niveles de riesgo de un grupo de dimensiones"""
    # Creamos un DF base con ceros
    df_dominio = pd.DataFrame({"Nivel": ORDEN_RIESGO, "Valor": [0.0] * len(ORDEN_RIESGO)})
    count = 0
    
    for dim in lista_dimensiones:
        if dim in resultados_intra and resultados_intra[dim]["Valor"].sum() > 0:
            df_dominio["Valor"] += resultados_intra[dim]["Valor"]
            count += 1
            
    if count > 0:
        df_dominio["Valor"] = df_dominio["Valor"] / count
    return df_dominio

def extraer_tabla_por_titulo(df, titulo_dimension, area_usuario):
    try:
        titulo_target = str(titulo_dimension).strip().upper()
        area_target = str(area_usuario).strip().upper()

        for r in range(len(df)):
            for c in range(df.columns.size):
                if titulo_target == str(df.iloc[r, c]).strip().upper():
                    columna_ancla = c
                    
                    # 1. MAPEAMOS DÓNDE QUEDÓ CADA RIESGO EN ESTA TABLA
                    mapeo_columnas = {}
                    # Escaneamos las filas cercanas al título para hallar los encabezados
                    for r_header in range(r, r + 5):
                        for c_busqueda in range(columna_ancla + 1, columna_ancla + 10):
                            if c_busqueda >= df.columns.size: break
                            txt = str(df.iloc[r_header, c_busqueda]).strip().lower()
                            
                            if "muy alto" in txt: mapeo_columnas["Riesgo muy alto"] = c_busqueda
                            elif "alto" in txt: mapeo_columnas["Riesgo alto"] = c_busqueda
                            elif "medio" in txt: mapeo_columnas["Riesgo medio"] = c_busqueda
                            elif "bajo" in txt: mapeo_columnas["Riesgo bajo"] = c_busqueda
                            elif "sin" in txt: mapeo_columnas["Sin Riesgo"] = c_busqueda
                    
                    # 2. BUSCAMOS LA FILA DEL ÁREA
                    for r_area in range(r, r + 100):
                        if r_area >= len(df): break
                        if str(df.iloc[r_area, columna_ancla]).strip().upper() == area_target:
                            
                            # 3. ARMAMOS LOS DATOS EN ORDEN LÓGICO
                            orden_visual = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto"]
                            valores = {nivel: pd.to_numeric(df.iloc[r_area, mapeo_columnas[nivel]], errors='coerce') 
                                      for nivel in orden_visual if nivel in mapeo_columnas}
                            
                            res_df = pd.DataFrame(list(valores.items()), columns=["Nivel", "Valor"]).fillna(0)
                            
                            # Ajuste de escala (0.15 -> 15.0)
                            if res_df["Valor"].max() <= 1.0:
                                res_df["Valor"] = res_df["Valor"] * 100
                                
                            return res_df
    except Exception as e:
        print(f"Error crítico en {titulo_dimension}: {e}")
    return pd.DataFrame(columns=["Nivel", "Valor"])

# --- Módulo de Recompensas ---
def procesar_dominio_recompensas(df_informe):
    """
    Solo procesa las 2 dimensiones de Recompensas. 
    Aquí puedes tunear cada una por separado.
    """
    return {
        "Reconocimiento y compensación": extraer_tabla_por_titulo(df_informe, "Reconocimiento y compensación"),
        "Recompensas de pertenencia y trabajo": extraer_tabla_por_titulo(df_informe, "Recompensas de pertenencia y trabajo")
    }