import pandas as pd
import unicodedata
import re

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

def extraer_dimension_informe_general(df, nombre_dimension, area_objetivo):
    import pandas as pd
    import unicodedata
    import re

    def limpiar_extremo(t):
        if pd.isna(t): return ""
        s = "".join(c for c in unicodedata.normalize('NFD', str(t)) if unicodedata.category(c) != 'Mn')
        return re.sub(r'[^A-Z0-9]', '', s.upper())

    t_dim = limpiar_extremo(nombre_dimension)
    t_area = limpiar_extremo(area_objetivo)
    
    # 1. LOCALIZAR LA DIMENSIÓN (Eje X)
    f_t, c_t = -1, -1
    for r in range(min(1000, df.shape[0])):
        for c in range(min(20, df.shape[1])):
            if t_dim in limpiar_extremo(df.iloc[r, c]):
                f_t, c_t = r, c
                break
        if f_t != -1: break

    if f_t == -1: 
        return pd.DataFrame([{"Nivel": n, "Valor": 0.0} for n in ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo"]])

    # 2. LOCALIZAR LA FILA DEL ÁREA (Eje Y)
    f_area = -1
    for r_idx in range(f_t, min(f_t + 500, df.shape[0])):
        for c_search in range(max(0, c_t-2), c_t + 5):
            val_limpio = limpiar_extremo(df.iloc[r_idx, c_search])
            if t_area != "" and t_area in val_limpio:
                if "TOTAL" not in val_limpio:
                    f_area = r_idx
                    break
        if f_area != -1: break

    # 3. EXTRACCIÓN QUIRÚRGICA (Solo los 5 valores de esta tabla)
    numeros = []
    if f_area != -1:
        for c_idx in range(c_t + 1, df.shape[1]):
            # Si ya recolectamos los 5 riesgos de esta dimensión, salimos antes de chocar con la otra tabla
            if len(numeros) == 5: 
                break
                
            val = df.iloc[f_area, c_idx]
            if pd.isna(val) or str(val).strip() == "" or "BLANCO" in str(val).upper():
                continue
            
            try:
                s_v = str(val).replace('%', '').replace(',', '.')
                m = re.search(r"(\d+\.?\d*)", s_v)
                if m:
                    n = float(m.group(1))
                    n = n * 100 if 0 < n <= 1.05 else n
                    if 0.01 < n < 99.9:
                        # Evitar duplicados por celdas combinadas
                        if not numeros or abs(numeros[-1] - n) > 0.05:
                            numeros.append(round(n, 2))
            except:
                continue

    # 4. ASIGNACIÓN SEGÚN ORDEN VISUAL (Bajo, Sin, Medio, Muy Alto, Alto)
    res = {n: 0.0 for n in ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo"]}
    
    if len(numeros) >= 5:
        res["Riesgo bajo"] = numeros[0]      # 21.57%
        res["Sin Riesgo"] = numeros[1]      # 29.41%
        res["Riesgo medio"] = numeros[2]     # 20.26%
        res["Riesgo muy alto"] = numeros[3]  # 18.30%
        res["Riesgo alto"] = numeros[4]      # 10.46%

    return pd.DataFrame([{"Nivel": k, "Valor": v} for k, v in res.items()])