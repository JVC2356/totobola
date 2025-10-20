import streamlit as st
import pandas as pd
from io import BytesIO

data = [["1", "X", "2"], ["X", "1", "2"]]
df = pd.DataFrame(data, columns=["Jogo 1", "Jogo 2", "Jogo 3"])

st.title("Teste Exportação Excel")

st.dataframe(df)

output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Apostas")
    workbook = writer.book
    worksheet = writer.sheets["Apostas"]
    header_format = workbook.add_format({
        'bold': True, 'valign': 'center', 'fg_color': '#FFFF00', 'border': 1
    })
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 10)

st.download_button(
    label="⬇️ Exportar Excel",
    data=output.getvalue(),
    file_name="teste.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)