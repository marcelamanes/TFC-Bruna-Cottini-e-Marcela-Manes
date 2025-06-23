# -*- coding: utf-8 -*- 
"""
Simulação usando distribuição Weibull Mínima
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parâmetros da distribuição Weibull Mínima
shape = 14291856.6301      # Parâmetro de forma (c)
loc = -1087518339.0944      # Parâmetro de localização
scale = 1087518653.8714     # Parâmetro de escala

# Configuração da simulação
num_dias = 1000
lambda_poisson = 1.48
turno_horas = 12
turno_minutos = turno_horas * 60

tempos_cirurgia_por_dia = []

# Simulação por dia
for _ in range(num_dias):
    num_pacientes = np.random.poisson(lam=lambda_poisson)

    if num_pacientes == 0:
        tempos_cirurgia = np.array([])
    else:
        tempos_cirurgia = stats.weibull_min.rvs(c=shape, loc=loc, scale=scale, size=num_pacientes)
    
    tempos_cirurgia_por_dia.append(tempos_cirurgia)

# Utilização por dia
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

todos_tempos = np.concatenate(tempos_cirurgia_por_dia)
tempos_totais_por_dia = [np.sum(tempos) for tempos in tempos_cirurgia_por_dia]

# Intervalos de confiança
ic_tempo_medio = stats.t.interval(0.95, len(todos_tempos)-1, loc=np.mean(todos_tempos), scale=stats.sem(todos_tempos))
print(f"IC 95% tempo médio: {ic_tempo_medio}")  

ic_utilizacao = stats.t.interval(0.95, len(utilizacao_por_dia)-1, loc=np.mean(utilizacao_por_dia), scale=stats.sem(utilizacao_por_dia))
print(f"IC 95% utilização média: {ic_utilizacao}")

# Estatísticas
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

def minutos_para_horas(minutos):
    return f"{minutos / 60:.2f} h"

estatisticas_tempo_total_diario = {
    "Média do tempo total diário": f"{np.mean(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.mean(tempos_totais_por_dia))}",
    "Desvio Padrão do tempo total diário": f"{np.std(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.std(tempos_totais_por_dia))}",
    "Percentil 95": f"{np.percentile(tempos_totais_por_dia, 95):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 95))}",
    "Percentil 99": f"{np.percentile(tempos_totais_por_dia, 99):.2f} min | {minutos_para_horas(np.percentile(tempos_totais_por_dia, 99))}",
    "Máximo tempo total diário": f"{np.max(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.max(tempos_totais_por_dia))}",
}

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

# Histograma
plt.figure(figsize=(10, 6))
plt.hist(todos_tempos, bins=30, color='green', alpha=0.7, edgecolor='black')
plt.xlabel('Tempo de Cirurgia (minutos)')
plt.ylabel('Frequência')
plt.title('Histograma dos Tempos de Cirurgia Simulados (Weibull Minima)')
plt.grid(True)
plt.show()
