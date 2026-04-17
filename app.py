import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SOS Master Deckbuilder", layout="wide")

# 1. BANCO DE DADOS COMPLETO (BASEADO EM SOS)
@st.cache_data
def get_full_database():
    data = [
        {"nome": "Daydream", "cor": "Branco", "cmc": 1, "tier": "B", "faculdade": "Silverquill"},
        {"nome": "Beledros Witherbloom", "cor": "Golgari", "cmc": 7, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Velomachus Lorehold", "cor": "Boros", "cmc": 7, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Galazeth Prismari", "cor": "Izzet", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Tanazir Quandrix", "cor": "Simic", "cmc": 5, "tier": "S", "faculdade": "Quandrix"},
        {"nome": "Shadrix Silverquill", "cor": "Orzhov", "cmc": 5, "tier": "S", "faculdade": "Silverquill"},
        {"nome": "Professor Onyx", "cor": "Preto", "cmc": 6, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Cultivate", "cor": "Verde", "cmc": 3, "tier": "A", "faculdade": "Arquivo"},
        {"nome": "Leonin Lightscribe", "cor": "Branco", "cmc": 2, "tier": "A", "faculdade": "Silverquill"},
        {"nome": "Archmage Emeritus", "cor": "Azul", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Dina, Soul Steeper", "cor": "Golgari", "cmc": 2, "tier": "B", "faculdade": "Witherbloom"},
        {"nome": "Killian, Ink Duelist", "cor": "Orzhov", "cmc": 2, "tier": "A", "faculdade": "Silverquill"}
    ]
    return pd.DataFrame(data)

# Inicializa a pool na memória
if 'pool' not in st.session_state:
    st.session_state.pool = []

db = get_full_database()

st.title("🧙‍♂️ SOS Master: Prerelease Helper")

st.header("1. Monte sua Pool")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Buscar na Lista SOS")
    # Menu de seleção das cartas
    nome_busca = st.selectbox("Selecione a carta:", [""] + sorted(db['nome'].tolist()))
    
    if st.button("Adicionar da Lista ➕"):
        if nome_busca != "":
            # AQUI ESTÁ A CORREÇÃO DA LINHA 62:
            selecionada = db[db['nome'] == nome_busca].to_dict('records')
            st.session_state.pool.append(selecionada)
            st.success(f"{nome_busca} adicionada!")
        else:
            st.warning("Selecione uma carta primeiro.")

with col2:
    st.subheader("Carta não está na lista?")
    with st.expander("Adicionar Manualmente"):
        m_nome = st.text_input("Nome")
        m_cor = st.selectbox("Cor", ["Branco", "Azul", "Preto", "Vermelho", "Verde", "Multicolor"])
        m_cmc = st.number_input("Custo", 0, 10, 2)
        m_tier = st.select_slider("Poder", ["S", "A", "B", "C", "D"], value="C")
        if st.button("Salvar Carta Manual ✅"):
            st.session_state.pool.append({"nome": m_nome, "cor": m_cor, "cmc": m_cmc, "tier": m_tier, "faculdade": "Manual"})
            st.toast(f"{m_nome} adicionada manualmente!")

# Exibição da Pool
if st.session_state.pool:
    df_pool = pd.DataFrame(st.session_state.pool)
    st.divider()
    
    c1, c2 = st.columns()
    with c1:
        st.subheader("Sua Seleção")
        st.dataframe(df_pool[['nome', 'cor', 'cmc', 'tier']], use_container_width=True)
        if st.button("🗑️ Limpar Pool"):
            st.session_state.pool = []
            st.rerun()
    with c2:
        st.subheader("Curva de Mana")
        fig, ax = plt.subplots()
        df_pool['cmc'].value_counts().sort_index().plot(kind='bar', ax=ax, color='teal')
        st.pyplot(fig)
