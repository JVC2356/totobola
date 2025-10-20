import streamlit as st
import csv
import io
import pandas as pd

# Função para carregar apostas
def carregar_apostas(file):
    reader = csv.reader(io.StringIO(file.getvalue().decode("utf-8")))
    headers = next(reader)
    apostas = list(zip(*reader))  # colunas viram apostas
    return apostas

# Conferir prémios
def conferir_premios(apostas, resultados):
    contagem = {i: 0 for i in range(10, 14)}
    detalhes = []

    for idx, aposta in enumerate(apostas):
        acertos = sum(1 for a, r in zip(aposta, resultados) if a == r)
        if acertos >= 10:
            contagem[acertos] += 1
        detalhes.append({
            "Nº Aposta": idx + 1,
            "Acertos": acertos,
            "Aposta": " ".join(aposta),
            "Prémio": f"{acertos} acertos" if acertos >= 10 else ""
        })

    return contagem, detalhes

# Cabeçalho bonito
st.set_page_config(page_title="Totobola Checker", layout="wide")
st.title("🏆 Sociedade Totobola – Conferência de Apostas")

# Upload do ficheiro
st.markdown("### 📂 Carregar ficheiro de apostas (`apostas_transpostas.csv`)")
ficheiro = st.file_uploader("Escolha o ficheiro CSV", type="csv")

# Inserção rápida dos 13 resultados
st.markdown("### 📝 Inserir os resultados oficiais")
entrada = st.text_input("Exemplo: `1 X 2 1 1 X 2 X 2 1 X 1 2`").strip().upper()
resultados = entrada.split()

# Verificar e processar
if st.button("✅ Verificar Prémios"):
    if len(resultados) != 13 or not all(r in ['1', 'X', '2'] for r in resultados):
        st.error("⚠️ Insira exatamente 13 resultados válidos (1, X ou 2).")
    elif not ficheiro:
        st.error("⚠️ Carregue o ficheiro de apostas.")
    else:
        apostas = carregar_apostas(ficheiro)
        contagem, detalhes = conferir_premios(apostas, resultados)

        st.success("🎉 Conferência concluída!")
        st.markdown("### 🎯 Resultado por categoria:")
        for acertos in sorted(contagem, reverse=True):
            st.write(f"**{acertos} acertos**: {contagem[acertos]}")

        # Mostrar tabela detalhada
        df = pd.DataFrame(detalhes)
        st.markdown("### 📋 Detalhes por Aposta")
        st.dataframe(df, use_container_width=True)

        # Botão para download
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Download resultados com prémios",
            data=csv_buffer.getvalue(),
            file_name="resultados_conferidos.csv",
            mime="text/csv"
        )