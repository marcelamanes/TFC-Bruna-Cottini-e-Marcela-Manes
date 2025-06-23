# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 11:36:58 2025
@author: Marcela Manes
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

def best_distribution(data):
    data = np.clip(data.dropna(), a_min=None, a_max=None)
    
    distributions = ['norm', 'expon', 'gamma', 'lognorm', 'beta',
                     'pearson3', 't', 'uniform', 'weibull_min', 'weibull_max']

    best_dist = None
    best_p = -1
    best_params = None
    
    for dist_name in distributions:
        dist = getattr(stats, dist_name)
        try:
            params = dist.fit(data)
            D, p_value = stats.kstest(data, dist_name, args=params)
            if p_value > best_p:
                best_dist = dist_name
                best_p = p_value
                best_params = params
        except Exception:
            continue
    
    return best_dist, best_p, best_params

def analisar_salas(file_path):
    # Carregar os dados da planilha
    df = pd.read_excel(file_path)
    
    df["Data"] = pd.to_datetime(df["Data"])
    df = df[~df["Data"].dt.weekday.isin([5, 6])]
    resultados = []

    for i in range(1, 10):  # Sala 01 a Sala 09
        sala = f"Sala {i:02d}"
        df_filtrado = df[
            (df["Sala cirúrgica"] == sala) &
            (df["Data"].dt.year == 2024)
        ]
        data = df_filtrado["Duração (min)"]

        if len(data) > 0:
            print(f"\n--- {sala} ---")
            print(f"{len(data)} registros encontrados")
            print(data.describe())

            dist, p, params = best_distribution(data)
            resultados.append({
                "Sala": sala,
                "Melhor distribuição": dist,
                "Valor p": p,
                "Parâmetros": params
            })

            print(f"Melhor distribuição: {dist}")
            print(f"Valor p: {p}")
            print(f"Parâmetros: {params}")
        else:
            print(f"\n--- {sala} ---")
            print("Sem dados para 2024.")

    return pd.DataFrame(resultados)

# Executar análise
file_path = "InputsTotais.xlsx"
resultado_df = analisar_salas(file_path)

# (Opcional) salvar resultados em CSV
# resultado_df.to_csv("melhores_distribuicoes_por_sala.csv", index=False)
