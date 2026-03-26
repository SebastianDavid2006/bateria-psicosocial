import pandas as pd

ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]

def buscar_coordenadas(df, texto_buscado):
    """Busca el título en las primeras 30 filas y devuelve (fila, columna)."""
    texto_buscado = texto_buscado.upper().strip()
    for r in range(min(30, df.shape[0])):
        for c in range(df.shape[1]):
            if texto_buscado in str(df.iloc[r, c]).upper():
                return r, c
    return -1, -1

def extraer_bloque_principal(df, titulo_tabla):
    fila_t, col_t = buscar_coordenadas(df, titulo_tabla)
    
    if fila_t == -1:
        return pd.DataFrame({"Nivel": ORDEN_RIESGO, "Valor": [0.0]*6})

    datos = []
    # Según tu imagen, los datos empiezan justo 1 fila abajo del título
    # El orden en el Excel es: Sin Riesgo, Riesgo bajo, Riesgo medio...
    etiquetas_orden_excel = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto", "Dato perdido"]
    
    for i, etiqueta in enumerate(etiquetas_orden_excel):
        try:
            # Leemos la celda que está 'i + 1' filas abajo del título
            val = df.iloc[fila_t + 1 + i, col_t]
            
            # Limpieza de datos: si es un string con espacios o vacío
            if pd.isna(val) or str(val).strip() == "":
                val = 0.0
            else:
                val = float(val)
        except:
            val = 0.0
        datos.append({"Nivel": etiqueta, "Valor": val})

    # Creamos el DF y lo reordenamos al estándar de la App (Muy alto arriba)
    df_res = pd.DataFrame(datos)
    return df_res.set_index("Nivel").reindex(ORDEN_RIESGO).reset_index().fillna(0)

def extraer_datos_psicosocial(df_raw, forma):
    """
    Busca los títulos exactos como aparecen en tu captura de pantalla.
    """
    return {
        "INTRALABORAL": extraer_bloque_principal(df_raw, f"Intralaboral {forma}"),
        "EXTRALABORAL": extraer_bloque_principal(df_raw, f"Extralaboral {forma}"),
        "ESTRÉS": extraer_bloque_principal(df_raw, f"Estrés {forma}")
    }

def extraer_subdimension(df_raw, nombre_sub):
    """Mismo motor para subdimensiones."""
    return extraer_bloque_principal(df_raw, nombre_sub)