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

import tkinter as tk
from tkinter import messagebox
import csv

# Função para carregar apostas do CSV
def carregar_apostas(filename="apostas_transpostas.csv"):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        apostas = list(zip(*reader))  # transpor: colunas viram listas
        return apostas

# Função para verificar prémios
def verificar_premios():
    resultados = [campo.get().strip().upper() for campo in campos]

    if len(resultados) != 13 or not all(r in ['1', 'X', '2'] for r in resultados):
        messagebox.showerror("Erro", "Insira 13 resultados válidos (1, X ou 2).")
        return

    apostas = carregar_apostas()

    contagem = {i: 0 for i in range(10, 14)}  # contamos de 10 a 13 acertos

    for aposta in apostas:
        acertos = sum(1 for a, r in zip(aposta, resultados) if a == r)
        if acertos >= 10:
            contagem[acertos] += 1

    resultado_msg = "\n".join([f"{acertos} acertos: {quant}" for acertos, quant in sorted(contagem.items(), reverse=True)])
    messagebox.showinfo("Resultados", resultado_msg)

# Interface gráfica
janela = tk.Tk()
janela.title("Conferir Totobola")

tk.Label(janela, text="Resultados Oficiais do Totobola (1, X ou 2)", font=("Arial", 14)).grid(row=0, column=0, columnspan=13, pady=10)

campos = []
for i in range(13):
    tk.Label(janela, text=f"Jogo {i+1}").grid(row=1, column=i)
    campo = tk.Entry(janela, width=3, justify='center')
    campo.grid(row=2, column=i)
    campos.append(campo)

btn = tk.Button(janela, text="Verificar Prémios", command=verificar_premios, bg="lightgreen")
btn.grid(row=3, column=0, columnspan=13, pady=15)

janela.mainloop()