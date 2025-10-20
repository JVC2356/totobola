import streamlit as st
import pandas as pd

st.title("Juntar dois ficheiros CSV (concatenação simples)")

# Upload dos dois ficheiros
ficheiro1 = st.file_uploader("Ficheiro 1", type="csv", key="f1")
ficheiro2 = st.file_uploader("Ficheiro 2", type="csv", key="f2")

if ficheiro1 and ficheiro2:
    # Ler os dois ficheiros
    df1 = pd.read_csv(ficheiro1)
    df2 = pd.read_csv(ficheiro2)

    # Verificar se têm as mesmas colunas
    if list(df1.columns) == list(df2.columns):
        # Concatenar os dois ficheiros
        df_final = pd.concat([df1, df2], ignore_index=True)

        st.subheader("Resultado: ficheiros combinados")
        st.dataframe(df_final)

        # Download do ficheiro final
        csv = df_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download do ficheiro combinado",
            data=csv,
            file_name="combinado.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ Os ficheiros não têm as mesmas colunas. Verifica os cabeçalhos.")