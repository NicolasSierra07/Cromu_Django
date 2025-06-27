import pandas as pd
import numpy as np

def analizar_datos(data):
    df = pd.DataFrame(data)

    # Ejemplo de datos esperados: [{'usuario': 'Juan', 'mes': 'Enero', 'monto': 30000}, ...]

    promedio_por_usuario = df.groupby('usuario')['monto'].mean().round(2).to_dict()
    total_por_usuario = df.groupby('usuario')['monto'].sum()
    ranking = total_por_usuario.sort_values(ascending=False).to_dict()

    resultado = {
        "promedios": promedio_por_usuario,
        "ranking": ranking
    }
    return resultado
