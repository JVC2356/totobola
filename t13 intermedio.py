import streamlit as st
import random
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Totobola Filtro", layout="centered")
st.title("🎯 Totobola - Filtro de Apostas Válidas com Percentagens")

TOTAL_JOGOS = 13
GRUPO1_IDX = range(0, 6)
GRUPO2_IDX = range(6, 13)
SIMBOLOS = ['1', 'X', '2']

# Palpites e percentagens
st.subheader("📥 Inserir palpites e confiança (em %)")

palpites_certos = []
confianças = []

for i in range(TOTAL_JOGOS):
    col1, col2 = st.columns([2, 1])
    with col1:
        palpite = st.selectbox(f"Jogo {i+1} - Palpite", SIMBOLOS, key=f"palpite_{i}")
    with col2:
        conf = st.slider("Confiança (%)", min_value=34, max_value=100, value=50, key=f"conf_{i}")
    palpites_certos.append(palpite)
    confianças.append(conf)

# Limites por símbolo em cada grupo
st.subheader("⚙️ Limites por símbolo (mínimo e máximo por grupo)")

def definir_limites_grupo(nome_grupo, max_jogos):
    st.markdown(f"### {nome_grupo}")
    limites = {}
    for s in SIMBOLOS:
        col1, col2 = st.columns(2)
        with col1:
            minimo = st.number_input(f"Mínimo '{s}'", min_value=0, max_value=max_jogos, value=0, key=f"{nome_grupo}_min_{s}")
        with col2:
            maximo = st.number_input(f"Máximo '{s}'", min_value=0, max_value=max_jogos, value=max_jogos, key=f"{nome_grupo}_max_{s}")
        limites[s] = (minimo, maximo)
    return limites

limites_g1 = definir_limites_grupo("Grupo 1 (Jogos 1 a 6)", 6)
limites_g2 = definir_limites_grupo("Grupo 2 (Jogos 7 a 13)", 7)

# Mostrar distribuição por jogo
st.subheader("📊 Distribuição de Probabilidades por Jogo")

for i in range(TOTAL_JOGOS):
    palpite = palpites_certos[i]
    conf = confianças[i]
    outros = [s for s in SIMBOLOS if s != palpite]
    restante = round((100 - conf) / 2, 1)
    probs = {
        palpite: conf,
        outros[0]: restante,
        outros[1]: restante
    }
    st.write(f"**Jogo {i+1}** → {probs}")

st.subheader("🎰 Gerar e Filtrar Apostas")
num_apostas = st.number_input("Quantas apostas gerar?", min_value=1000, max_value=100000, value=10000, step=1000)
max_final = 200

def gerar_aposta_com_probabilidades():
    aposta = []
    for i in range(TOTAL_JOGOS):
        palpite = palpites_certos[i]
        conf = confianças[i]
        outros = [s for s in SIMBOLOS if s != palpite]
        restante = (100 - conf) / 2
        pesos = {
            palpite: conf,
            outros[0]: restante,
            outros[1]: restante
        }
        escolhas = list(pesos.keys())
        probabilidade = [pesos[s] / 100 for s in escolhas]
        escolha = random.choices(escolhas, weights=probabilidade, k=1)[0]
        aposta.append(escolha)
    return aposta

def respeita_intervalos(aposta, grupo_idx, limites):
    contagem = {'1': 0, 'X': 0, '2': 0}
    for i in grupo_idx:
        contagem[aposta[i]] += 1
    for s in SIMBOLOS:
        minimo, maximo = limites[s]
        if not (minimo <= contagem[s] <= maximo):
            return False
    return True

if st.button("⚙️ Gerar Apostas Válidas"):
    apostas_validas = []

    for _ in range(num_apostas):
        aposta = gerar_aposta_com_probabilidades()

        if not respeita_intervalos(aposta, GRUPO1_IDX, limites_g1):
            continue
        if not respeita_intervalos(aposta, GRUPO2_IDX, limites_g2):
            continue

        acertos_grupo1 = sum(aposta[i] == palpites_certos[i] for i in GRUPO1_IDX)
        acertos_grupo2 = sum(aposta[i] == palpites_certos[i] for i in GRUPO2_IDX)

        if acertos_grupo1 in [3, 4] and acertos_grupo2 in [3, 4]:
            apostas_validas.append(aposta)

        if len(apostas_validas) >= max_final:
            break

    if apostas_validas:
        st.success(f"✅ {len(apostas_validas)} apostas válidas encontradas!")

        df = pd.DataFrame(apostas_validas, columns=[f"Jogo {i+1}" for i in range(TOTAL_JOGOS)])
        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Apostas')
        st.download_button(
            label="⬇️ Exportar para Excel (.xlsx)",
            data=output.getvalue(),
            file_name="apostas_validas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("❌ Nenhuma aposta válida encontrada com os critérios definidos.")