import streamlit as st
import pandas as pd

st.title("Completar dados a partir do ficheiro principal")

# Upload dos ficheiros
ficheiro_principal = st.file_uploader("Carrega o ficheiro principal", type="csv", key="principal")
ficheiro_parcial = st.file_uploader("Carrega o ficheiro com nomes", type="csv", key="parcial")

if ficheiro_principal and ficheiro_parcial:
    # Carregar ficheiros
    df_principal = pd.read_csv(ficheiro_principal)
    df_parcial = pd.read_csv(ficheiro_parcial)

    # 🔍 Verificar duplicados no campo "nome"
    duplicados = df_principal[df_principal.duplicated(subset='nome', keep=False)]
    if not duplicados.empty:
        st.warning("⚠️ Existem nomes duplicados no ficheiro principal:")
        st.dataframe(duplicados)

        # ✅ Botão para remover duplicados
        if st.button("Remover duplicados (manter apenas o primeiro)"):
            df_principal = df_principal.drop_duplicates(subset='nome', keep='first')
            st.success("✅ Duplicados removidos. Apenas a primeira ocorrência de cada nome foi mantida.")

    # Selecionar só as colunas que interessam
    colunas_utilizar = ["nome", "morada", "pais"]
    df_filtrado = df_principal[colunas_utilizar]

    # Fazer o merge pelo campo "nome"
    df_resultado = pd.merge(df_parcial, df_filtrado, on="nome", how="left")

    # Mostrar o resultado
    st.subheader("Resultado do ficheiro preenchido")
    st.dataframe(df_resultado)

    # Download do CSV resultante
    csv = df_resultado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download do CSV completo",
        data=csv,
        file_name="completo.csv",
        mime="text/csv"
    )