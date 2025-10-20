import re
import csv

# Abrir o ficheiro
with open("ficheiro.txt", "r", encoding="latin-1") as f:
    linhas = f.readlines()

linha_aposta = re.compile(r"^\s*(\d{1,2})\.\s+((?:[X12]\s+){2,})")
apostas_brutas = []

# Extrair apostas com no máximo 10 resultados
for linha in linhas:
    match = linha_aposta.match(linha)
    if match:
        resultados = match.group(2).strip().split()
        apostas_brutas.append(resultados[:10])

# Agora vamos formar apostas verticais:
# Cada aposta é composta por 13 linhas consecutivas (formando colunas de 13 jogos)
apostas_verticais = []
for i in range(0, len(apostas_brutas), 13):
    bloco = apostas_brutas[i:i+13]
    if len(bloco) == 13:  # só usamos blocos completos de 13 linhas
        for j in range(len(bloco[0])):  # normalmente até 10 apostas por linha
            nova_aposta = [bloco[k][j] for k in range(13)]
            apostas_verticais.append(nova_aposta)

# Escrever o CSV com colunas numeradas sequencialmente
with open("apostas_transpostas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([str(i+1) for i in range(len(apostas_verticais))])  # cabeçalho 1,2,3,...
    for i in range(13):  # 13 linhas por jogo
        linha = [aposta[i] for aposta in apostas_verticais]
        writer.writerow(linha)

import pandas as pd
df = pd.read_csv("apostas_transpostas.csv")
df.to_excel("apostas_transpostas.xlsx", index=False)