import pandas as pd

ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]

def buscar_coordenadas(df, texto_buscado):
    """Busca el título en todo el DataFrame y devuelve (fila, columna)."""
    texto_buscado = texto_buscado.upper().strip()
    # Ampliamos el rango de búsqueda a todo el DF para encontrar subdimensiones lejanas
    for r in range(df.shape[0]):
        for c in range(df.shape[1]):
            val_actual = str(df.iloc[r, c]).upper()
            if texto_buscado == val_actual: # Buscamos coincidencia exacta para evitar errores
                return r, c
    return -1, -1

def extraer_bloque_principal(df, titulo_tabla):
    fila_t, col_t = buscar_coordenadas(df, titulo_tabla)
    
    if fila_t == -1:
        # Si no lo encuentra, devolvemos ceros para no romper la gráfica
        return pd.DataFrame({"Nivel": ORDEN_RIESGO, "Valor": [0.0]*6})

    datos = []
    # El orden en el Excel es: Sin Riesgo (fila+1), Riesgo bajo (fila+2)...
    etiquetas_orden_excel = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto", "Dato perdido"]
    
    for i, etiqueta in enumerate(etiquetas_orden_excel):
        try:
            # Según tu imagen, los valores están en la columna de al lado o la misma. 
            # Si el título está en la celda, el valor está 1 fila abajo.
            val = df.iloc[fila_t + 1 + i, col_t]
            
            if pd.isna(val) or str(val).strip() == "":
                val = 0.0
            else:
                # Convertimos a float. Si viene como 0.13 (13%), lo manejamos en la vista.
                val = float(val)
        except:
            val = 0.0
        datos.append({"Nivel": etiqueta, "Valor": val})

    df_res = pd.DataFrame(datos)
    # Reordenamos al estándar (Muy alto arriba)
    return df_res.set_index("Nivel").reindex(ORDEN_RIESGO).reset_index().fillna(0)

def extraer_datos_psicosocial(df_raw, forma):
    """Extrae las dimensiones principales de la hoja Gráficas."""
    return {
        "INTRALABORAL": extraer_bloque_principal(df_raw, f"Intralaboral {forma}"),
        "EXTRALABORAL": extraer_bloque_principal(df_raw, f"Extralaboral {forma}"),
        "ESTRÉS": extraer_bloque_principal(df_raw, f"Estrés {forma}")
    }

def extraer_subdimension(df_raw, nombre_sub):
    """
    Extrae subdimensiones (ej. 'Demandas emocionales') de la hoja Informe General.
    """
    return extraer_bloque_principal(df_raw, nombre_sub)