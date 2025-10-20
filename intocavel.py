import re
import csv

# Abrir ficheiro com codificação mais permissiva
with open("ficheiro.txt", "r", encoding="latin-1") as f:
    linhas = f.readlines()

apostas_brutas = []
linha_aposta = re.compile(r"^\s*(\d{1,2})\.\s+((?:[X12]\s+){2,})")

for linha in linhas:
    match = linha_aposta.match(linha)
    if match:
        resultados = match.group(2).strip().split()
        apostas_brutas.append(resultados[:10])  # máximo 10 elementos

# Agrupar em blocos de 13 linhas
blocos = [apostas_brutas[i:i+13] for i in range(0, len(apostas_brutas), 13)]

# Transpor blocos: linha 1 de todos os blocos, linha 2 de todos os blocos, etc.
apostas_transpostas = []
for i in range(13):  # linhas 1 a 13
    linha_transposta = []
    for bloco in blocos:
        if i < len(bloco):  # segurança para blocos incompletos
            linha_transposta.append(" ".join(bloco[i]))
        else:
            linha_transposta.append("")
    apostas_transpostas.append(linha_transposta)

# Escrever no CSV
with open("apostas_transpostas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([f"Aposta {i+1}" for i in range(len(blocos))])  # cabeçalho
    for linha in apostas_transpostas:
        writer.writerow(linha)