# analise.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("📊 Análise de Dados Simples")

    uploaded_file = st.file_uploader("Carrega um ficheiro CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Ficheiro carregado via upload.")
    else:
        try:
            df = pd.read_csv("analise.csv")
            st.info("Sem upload — a carregar ficheiro local 'analise.csv'.")
        except FileNotFoundError:
            st.error("Nenhum ficheiro carregado e 'analise.csv' não existe.")
            st.stop()

    st.write("📄 Primeiras linhas dos dados:")
    st.dataframe(df.head())

    st.write("📈 Estatísticas descritivas:")
    st.write(df.describe())
