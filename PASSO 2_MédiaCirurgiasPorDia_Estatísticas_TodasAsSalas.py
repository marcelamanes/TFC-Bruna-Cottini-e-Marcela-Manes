# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 08:12:09 2025

@author: bruna
"""

import pandas as pd

# Carregar a planilha
file_path = "InputsTotais.xlsx"
xls = pd.ExcelFile(file_path)

# Carregar os dados da aba "Dados Inputs"
df = pd.read_excel(xls, sheet_name="Dados Inputs")

# Garantir que a coluna "Data" seja do tipo datetime
df["Data"] = pd.to_datetime(df["Data"])

# Remover sábados (5) e domingos (6)
df = df[~df["Data"].dt.weekday.isin([5, 6])]

# Loop para salas de Sala 01 até Sala 09
for i in range(1, 10):
    sala = f"Sala {i:02d}"  # Gera "Sala 01", "Sala 02", ..., "Sala 09"
    df_filtrado = df[df["Sala cirúrgica"] == sala]

    # Contar o número de cirurgias por dia após o filtro
    cirurgias_por_dia = df_filtrado["Data"].value_counts()

    # Calcular a média de cirurgias por dia com os dados filtrados
    media = cirurgias_por_dia.mean()

    print(f"{sala}: média de {media:.2f} cirurgias por dia")

import scipy.stats as stats
import numpy as np

print("\n---------------- Estatísticas Detalhadas por Sala ----------------\n")

for i in range(1, 10):
    sala = f"Sala {i:02d}"
    df_filtrado = df[df["Sala cirúrgica"] == sala]

    if df_filtrado.empty:
        print(f"{sala}: Sem dados disponíveis.\n")
        continue

    print(f"\n====== {sala} ======\n")

    # Tempo total de cirurgia por dia
    tempo_total_por_dia = df_filtrado.groupby("Data")["Duração (min)"].sum()

    # Utilização diária (%)
    utilizacao_diaria = (tempo_total_por_dia / 720 * 100).round(2)

    # Média geral de utilização
    media_utilizacao = utilizacao_diaria.mean().round(2)

    print(f"Utilização diária (%):")
    print(utilizacao_diaria)
    print(f"\nMédia geral de utilização: {media_utilizacao}%")

    # Intervalo de confiança para a utilização diária
    utilizacoes = utilizacao_diaria.values
    media_util = utilizacoes.mean()
    sem_util = stats.sem(utilizacoes)
    ic_utilizacao = stats.t.interval(0.95, len(utilizacoes)-1, loc=media_util, scale=sem_util)

    print(f"\nIC 95% para a média de utilização diária: {ic_utilizacao[0]:.2f}% a {ic_utilizacao[1]:.2f}%")

    # IC tempo total diário
    media_tempo_diario = tempo_total_por_dia.mean()
    sem_tempo_diario = stats.sem(tempo_total_por_dia)
    ic_tempo_diario = stats.t.interval(0.95, len(tempo_total_por_dia)-1,
                                       loc=media_tempo_diario,
                                       scale=sem_tempo_diario)

    print(f"\nIC 95% para tempo total diário: {ic_tempo_diario[0]:.2f} a {ic_tempo_diario[1]:.2f} minutos")

    # Percentis da utilização diária
    percentis_utilizacao = {
        "Média (%)": np.mean(utilizacao_diaria),
        "Mediana (%)": np.median(utilizacao_diaria),
        "Percentil 25 (%)": np.percentile(utilizacao_diaria, 25),
        "Percentil 75 (%)": np.percentile(utilizacao_diaria, 75),
        "Percentil 95 (%)": np.percentile(utilizacao_diaria, 95),
        "Percentil 99 (%)": np.percentile(utilizacao_diaria, 99)
    }

    print("\nEstatísticas da Utilização Diária (%):")
    for k, v in percentis_utilizacao.items():
        print(f"{k}: {v:.2f}%")

    # Percentis do tempo total diário
    percentis_tempo_diario = {
        "Média (min)": np.mean(tempo_total_por_dia),
        "Mediana (min)": np.median(tempo_total_por_dia),
        "Percentil 25 (min)": np.percentile(tempo_total_por_dia, 25),
        "Percentil 75 (min)": np.percentile(tempo_total_por_dia, 75),
        "Percentil 95 (min)": np.percentile(tempo_total_por_dia, 95),
        "Percentil 99 (min)": np.percentile(tempo_total_por_dia, 99),
        "Tempo Máximo da Simulação (min)": tempo_total_por_dia.max()
    }

    print("\nEstatísticas do Tempo Total Diário (min):")
    for k, v in percentis_tempo_diario.items():
        print(f"{k}: {v:.2f}")

    # print('--------------')
    # for z in utilizacoes:
    #     if z > 1:
    #         print(z)

    print('--------------')
     
    maiores_que_um = [z for z in utilizacoes if z > 100]
    print("Total de valores maiores que 100:", len(maiores_que_um))

    porcentagem = len(maiores_que_um) / len(utilizacoes) * 100
    print(f"{porcentagem:.2f}% dos valores são maiores que 100%")

print("\n---------------- Fim das Estatísticas ----------------")
