# -*- coding: utf-8 -*- 
"""
Created on Thu May 29 17:59:20 2025

@author: bruna
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parâmetros da distribuição Pearson type III
skew = 0.9154
loc = 200.8244
scale = 101.4048

# Configuração da simulação
num_dias = 1000             # Número de dias simulados
lambda_poisson = 1.50     # Média de pacientes por dia
turno_horas = 12
turno_minutos = turno_horas * 60

# Lista para armazenar os tempos de cirurgia por dia
tempos_cirurgia_por_dia = []

# Simulação para cada dia
for _ in range(num_dias):
    num_pacientes = np.random.poisson(lam=lambda_poisson)
    
    if num_pacientes == 0:
        tempos_cirurgia = np.array([])  # Nenhum paciente no dia
    else:
        # Gerar tempos com distribuição Pearson type III (sem truncamento)
        tempos_cirurgia = stats.pearson3.rvs(skew, loc=loc, scale=scale, size=num_pacientes)
    
    tempos_cirurgia_por_dia.append(tempos_cirurgia)

# Cálculo da utilização por dia
utilizacao_por_dia = [np.sum(tempos) / turno_minutos for tempos in tempos_cirurgia_por_dia]

print('--------------')
for z in utilizacao_por_dia:
    if z > 1:
        print(z)
print('--------------')

maiores_que_um = [z for z in utilizacao_por_dia if z > 1]
print("Total de valores maiores que 1:", len(maiores_que_um))

porcentagem = len(maiores_que_um) / len(utilizacao_por_dia) * 100
print(f"{porcentagem:.2f}% dos valores são maiores que 1")

# Flatten todos os tempos de cirurgia para estatísticas
todos_tempos = np.concatenate(tempos_cirurgia_por_dia)
tempos_totais_por_dia = [np.sum(tempos) for tempos in tempos_cirurgia_por_dia]

# Intervalo de confiança 95% - tempo médio
ic_tempo_medio = stats.t.interval(0.95, len(todos_tempos)-1, loc=np.mean(todos_tempos), scale=stats.sem(todos_tempos))
print(f"IC 95% tempo médio: {ic_tempo_medio}")  

# Intervalo de confiança 95% - utilização média
ic_utilizacao = stats.t.interval(0.95, len(utilizacao_por_dia)-1, loc=np.mean(utilizacao_por_dia), scale=stats.sem(utilizacao_por_dia))
print(f"IC 95% utilização média: {ic_utilizacao}")

# Estatísticas dos tempos de cirurgia (todos os pacientes)
estatisticas_tempo_total = {
    "Média (min)": np.mean(todos_tempos),
    "Desvio Padrão (min)": np.std(todos_tempos),
    "Mediana (min)": np.median(todos_tempos),
    "Percentil 25 (min)": np.percentile(todos_tempos, 25),
    "Percentil 75 (min)": np.percentile(todos_tempos, 75),
    "Percentil 95 (min)": np.percentile(todos_tempos, 95),
    "Percentil 99 (min)": np.percentile(todos_tempos, 99),
    "Média de Utilização": np.mean(utilizacao_por_dia),
    "max (min)": np.max(todos_tempos)
}

# Função para converter minutos em horas formatadas
def minutos_para_horas(minutos):
    horas = minutos / 60
    return f"{horas:.2f} h"

# Estatísticas do tempo total diário (em minutos e horas)
estatisticas_tempo_total_diario = {
    "Média do tempo total diário": f"{np.mean(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.mean(tempos_totais_por_dia))}",
    "Desvio Padrão do tempo total diário": f"{np.std(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.std(tempos_totais_por_dia))}",
    "Percentil 95": f"{np.percentile(tempos_totais_por_dia, 95):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 95))}",
    "Percentil 99": f"{np.percentile(tempos_totais_por_dia, 99):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 99))}",
    "Máximo tempo total diário": f"{np.max(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.max(tempos_totais_por_dia))}",
}

# IC 95% para o tempo total diário (minutos)
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

# Médias por dia (ignora dias sem pacientes)
medias_por_dia = [np.mean(dia) if dia.size > 0 else np.nan for dia in tempos_cirurgia_por_dia]

# Histograma dos tempos de cirurgia simulados
plt.figure(figsize=(10, 6))
plt.hist(todos_tempos, bins=30, color='green', alpha=0.7, edgecolor='black')
plt.xlabel('Tempo de Cirurgia (minutos)')
plt.ylabel('Frequência')
plt.title('Histograma dos Tempos de Cirurgia Simulados (Distribuição Pearson type III)')
plt.grid(True)
plt.show()