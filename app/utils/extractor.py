import pandas as pd

# Definición global del orden para que sea consistente
ORDEN_RIESGO = ["Riesgo muy alto", "Riesgo alto", "Riesgo medio", "Riesgo bajo", "Sin Riesgo", "Dato perdido"]

def extraer_datos_psicosocial(df_raw, forma):
    """
    Extrae los conteos de personas por dimensión desde el Excel.
    """
    resultados = {}
    columnas_map = {
        "INTRALABORAL": 1 if forma == "A" else 2,
        "EXTRALABORAL": 3 if forma == "A" else 4,
        "ESTRÉS": 7 if forma == "A" else 8
    }
    
    for dim, col_idx in columnas_map.items():
        datos = []
        col_etiquetas = 0 if col_idx < 5 else 6
        
        # Localizar el inicio de la tabla (Busca 'Sin Riesgo')
        fila_inicio = -1
        for r in range(min(35, df_raw.shape[0])):
            if "SIN RIESGO" in str(df_raw.iloc[r, col_etiquetas]).upper():
                fila_inicio = r
                break
        
        if fila_inicio != -1:
            etiquetas_excel = ["Sin Riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Riesgo muy alto", "Dato perdido"]
            for i, etiqueta in enumerate(etiquetas_excel):
                try:
                    val = float(df_raw.iloc[fila_inicio + i, col_idx])
                    val = 0 if pd.isna(val) else val
                except: val = 0
                datos.append({"Nivel": etiqueta, "Valor": val})
            
            df_res = pd.DataFrame(datos).set_index("Nivel").reindex(ORDEN_RIESGO).reset_index().fillna(0)
            resultados[dim] = df_res
            
    return resultados