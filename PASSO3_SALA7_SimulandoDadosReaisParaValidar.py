# -*- coding: utf-8 -*- 
"""
Simulação usando distribuição Lognormal
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parâmetros da distribuição Lognormal
shape = 0.6240      # Parâmetro de forma (s)
loc = 8.1092     # Parâmetro de localização
scale = 26.0918     # Parâmetro de escala

# Configuração da simulação
num_dias = 1000             # Número de dias simulados
lambda_poisson = 5.62       # Média de pacientes por dia
turno_horas = 12
turno_minutos = turno_horas * 60

tempos_cirurgia_por_dia = []

# Simulação por dia
for _ in range(num_dias):
    num_pacientes = np.random.poisson(lam=lambda_poisson)
    
    if num_pacientes == 0:
        tempos_cirurgia = np.array([])
    else:
        tempos_cirurgia = stats.lognorm.rvs(s=shape, loc=loc, scale=scale, size=num_pacientes)
    
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

# Conversor minutos → horas
def minutos_para_horas(minutos):
    horas = minutos / 60
    return f"{horas:.2f} h"

# Estatísticas por dia
estatisticas_tempo_total_diario = {
    "Média do tempo total diário": f"{np.mean(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.mean(tempos_totais_por_dia))}",
    "Desvio Padrão do tempo total diário": f"{np.std(tempos_totais_por_dia):.2f} min | {minutos_para_horas(np.std(tempos_totais_por_dia))}",
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
plt.hist(todos_tempos, bins=30, color='purple', alpha=0.7, edgecolor='black')
plt.xlabel('Tempo de Cirurgia (minutos)')
plt.ylabel('Frequência')
plt.title('Histograma dos Tempos de Cirurgia Simulados (Distribuição Lognormal)')
plt.grid(True)
plt.show()
