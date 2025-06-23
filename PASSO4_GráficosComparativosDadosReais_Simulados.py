# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
Created on Thu Apr  3 08:12:09 2025

@author: bruna
"""
import seaborn as sns
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
    #utilizacao_diaria = (tempo_total_por_dia / 720 * 100).round(2)
# Definindo os turnos por sala em minutos
    turnos_por_sala = {
        "Sala 01": 720,
        "Sala 02": 720,
       "Sala 03": 1440,
       "Sala 04": 720,
       "Sala 05": 900,
       "Sala 06": 900,
       "Sala 07": 720,
       "Sala 08": 1440,
       "Sala 09": 720
       }

# Obter o tempo de turno para a sala atual
    tempo_turno = turnos_por_sala.get(sala, 720)  # usa 720 como padrão, se a sala não estiver no dicionário

# Utilização diária (%)
    utilizacao_diaria = (tempo_total_por_dia / tempo_turno * 100).round(2)

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

"""
Simulação usando distribuição Gamma
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parâmetros da distribuição Gamma
a = 2.37        # Forma
loc = 9.04      # Localização
scale = 59.35   # Escala

# Configuração da simulação
num_dias = 1000             # Número de dias simulados
lambda_poisson = 2.67      # Média de pacientes por dia
turno_horas = 12
turno_minutos = turno_horas * 60

tempos_cirurgia_por_dia = []

# Simulação por dia
for _ in range(num_dias):
    num_pacientes = np.random.poisson(lam=lambda_poisson)
    
    if num_pacientes == 0:
        tempos_cirurgia = np.array([])
    else:
        tempos_cirurgia = stats.gamma.rvs(a=a, loc=loc, scale=scale, size=num_pacientes)
    
    tempos_cirurgia_por_dia.append(tempos_cirurgia)

# Utilização por dia
utilizacao_por_dia = [np.sum(tempos) / turno_minutos for tempos in tempos_cirurgia_por_dia]

# print('--------------')
# for z in utilizacao_por_dia:
#     if z > 1:
#         print(z)
# print('--------------')

maiores_que_um = [z for z in utilizacao_por_dia if z > 1]
print("Total de valores maiores que 1:", len(maiores_que_um))

porcentagem = len(maiores_que_um) / len(utilizacao_por_dia) * 100
print(f"{porcentagem:.2f}% dos valores são maiores que 1")

# Todos os tempos e totais por dia
todos_tempos = np.concatenate(tempos_cirurgia_por_dia)
tempos_totais_por_dia = [np.sum(tempos) for tempos in tempos_cirurgia_por_dia]

# Intervalo de confiança para o tempo médio
ic_tempo_medio = stats.t.interval(0.95, len(todos_tempos)-1, loc=np.mean(todos_tempos), scale=stats.sem(todos_tempos))
print(f"IC 95% tempo médio: {ic_tempo_medio}")  

# Intervalo de confiança para a utilização
ic_utilizacao = stats.t.interval(0.95, len(utilizacao_por_dia)-1, loc=np.mean(utilizacao_por_dia), scale=stats.sem(utilizacao_por_dia))
print(f"IC 95% utilização média: {ic_utilizacao}")

# Estatísticas gerais
estatisticas_tempo_total = {
    #"Média (min)": np.mean(todos_tempos),
    #"Desvio Padrão (min)": np.std(todos_tempos),
    #"Mediana (min)": np.median(todos_tempos),
    #"Percentil 25 (min)": np.percentile(todos_tempos, 25),
    #"Percentil 75 (min)": np.percentile(todos_tempos, 75),
    #"Percentil 95 (min)": np.percentile(todos_tempos, 95),
    #"Percentil 99 (min)": np.percentile(todos_tempos, 99),
    "Média de Utilização": np.mean(utilizacao_por_dia),
    "max (min)": np.max(todos_tempos)
}

# Conversor minutos → horas
def minutos_para_horas(minutos):
    horas = minutos / 60
    return f"{horas:.2f} h"

# Estatísticas por dia
estatisticas_tempo_total_diario = {
    "Média do tempo total diário": f"{np.mean(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.mean(tempos_totais_por_dia))}",
    #"Desvio Padrão do tempo total diário": f"{np.std(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.std(tempos_totais_por_dia))}",
    "Percentil 95": f"{np.percentile(tempos_totais_por_dia, 95):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 95))}",
    "Percentil 99": f"{np.percentile(tempos_totais_por_dia, 99):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 99))}",
    "Máximo tempo total diário": f"{np.max(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.max(tempos_totais_por_dia))}",
}

# IC 95% para tempo total por dia
ic_tempo_total = stats.t.interval(
    confidence=0.95,
    df=len(tempos_totais_por_dia)-1,
    loc=np.mean(tempos_totais_por_dia),
    scale=stats.sem(tempos_totais_por_dia)
)

estatisticas_tempo_total_diario["IC 95% do tempo total diário"] = (
    f"[{ic_tempo_total[0]:.2f}, {ic_tempo_total[1]:.2f}] min | "
    f"[{minutos_para_horas(ic_tempo_total[0])}, {minutos_para_horas(ic_tempo_total[1])}]"
)

print(estatisticas_tempo_total)
print("****************************************************************")
print("\nEstatísticas do Tempo Total Diário (Minutos e Horas):")
for key, value in estatisticas_tempo_total_diario.items():
    print(f"{key}: {value}")

# Médias por dia
medias_por_dia = [np.mean(dia) if dia.size > 0 else np.nan for dia in tempos_cirurgia_por_dia]

# Histograma dos tempos simulados
plt.figure(figsize=(10, 6))
plt.hist(todos_tempos, bins=30, color='green', alpha=0.7, edgecolor='black')
plt.xlabel('Tempo de Cirurgia (minutos)')
plt.ylabel('Frequência')
plt.title('Histograma dos Tempos de Cirurgia Simulados (Distribuição Gamma)')
plt.grid(True)
plt.show()

# -*- coding: utf-8 -*-
# Gráfico comparativo entre dados reais e simulados - Sala 5 (versão curvas)

# Filtrar dados reais da Sala 5
sala5_real = df[df["Sala cirúrgica"] == "Sala 05"]
tempos_reais = sala5_real["Duração (min)"].values

# Gerar dados simulados com mesma quantidade que os reais para comparação
dados_simulados = stats.gamma.rvs(a=a, loc=loc, scale=scale, size=len(tempos_reais))

# Criar figura
plt.figure(figsize=(12, 6))

# Plotar KDE dos dados reais
sns.kdeplot(tempos_reais, color='blue', linewidth=2, label='Dados Reais')

# Plotar KDE dos dados simulados
sns.kdeplot(dados_simulados, color='orange', linewidth=2, linestyle='--', 
            label='Dados Simulados (Gamma)')

# Plotar PDF da distribuição Gamma teórica
x = np.linspace(min(tempos_reais.min(), dados_simulados.min()),
                max(tempos_reais.max(), dados_simulados.max()), 1000)
pdf = stats.gamma.pdf(x, a=a, loc=loc, scale=scale)
plt.plot(x, pdf, 'r-', lw=2, label='Distribuição Gamma Teórica')

# Adicionar detalhes ao gráfico
plt.title('Comparação entre Distribuições - Sala 5 (Curvas)', fontsize=14)
plt.xlabel('Tempo de Cirurgia (minutos)', fontsize=12)
plt.ylabel('Densidade de Probabilidade', fontsize=12)
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, alpha=0.3)

# Adicionar informações sobre os parâmetros
param_text = f'Parâmetros Gamma:\na (forma) = {a:.2f}\nloc (localização) = {loc:.2f}\nscale (escala) = {scale:.2f}'
plt.text(0.95, 0.95, param_text, transform=plt.gca().transAxes,
         ha='right', va='top', bbox=dict(facecolor='white', alpha=0.8))

# Mostrar estatísticas descritivas
stats_text = f'Dados Reais:\nMédia = {np.mean(tempos_reais):.1f} min\nDesvio = {np.std(tempos_reais):.1f} min\n\n'\
             f'Dados Simulados:\nMédia = {np.mean(dados_simulados):.1f} min\nDesvio = {np.std(dados_simulados):.1f} min'
plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes,
         ha='left', va='top', bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

