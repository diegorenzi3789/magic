import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SOS Master Deckbuilder", layout="wide")

# 1. BANCO DE DADOS (Baseado na MTGStocks SOS)
@st.cache_data
def get_full_database():
    data = [
        # --- Raras e Míticas de Peso (Base MTGStocks) ---
        {"nome": "Beledros Witherbloom", "cor": "Golgari", "cmc": 7, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Velomachus Lorehold", "cor": "Boros", "cmc": 7, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Galazeth Prismari", "cor": "Izzet", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Tanazir Quandrix", "cor": "Simic", "cmc": 5, "tier": "S", "faculdade": "Quandrix"},
        {"nome": "Shadrix Silverquill", "cor": "Orzhov", "cmc": 5, "tier": "S", "faculdade": "Silverquill"},
        {"nome": "Professor Onyx", "cor": "Preto", "cmc": 6, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Daydream", "cor": "Branco", "cmc": 1, "tier": "B", "faculdade": "Silverquill"},
        {"nome": "Mila, Crafty Companion", "cor": "Branco", "cmc": 3, "tier": "A", "faculdade": "Neutral"},
        {"nome": "Blex, Vexing Pest", "cor": "Verde", "cmc": 3, "tier": "A", "faculdade": "Witherbloom"},
        # --- Arquivo Místico (SOA) ---
        {"nome": "Time Warp", "cor": "Azul", "cmc": 5, "tier": "S", "faculdade": "Arquivo"},
        {"nome": "Tainted Pact", "cor": "Preto", "cmc": 2, "tier": "A", "faculdade": "Arquivo"},
        {"nome": "Inquisition of Kozilek", "cor": "Preto", "cmc": 1, "tier": "A", "faculdade": "Arquivo"},
        {"nome": "Cultivate", "cor": "Verde", "cmc": 3, "tier": "A", "faculdade": "Arquivo"},
    ]
    return pd.DataFrame(data)

# Inicializar a pool na sessão do usuário
if 'pool' not in st.session_state:
    st.session_state.pool = []

db = get_full_database()

st.title("🧙‍♂️ Secrets of Strixhaven: Full Set Helper")

# --- AREA DE ADIÇÃO ---
st.header("1. Monte sua Pool do Pre-release")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Buscar na Lista SOS")
    nome_busca = st.selectbox("Selecione a carta:", [""] + sorted(db['nome'].tolist()))
    if st.button("Adicionar da Lista ➕") and nome_busca != "":
        carta = db[db['nome'] == nome_busca].iloc.to_dict()
        st.session_state.pool.append(carta)
        st.toast(f"{nome_busca} adicionada!")

with col2:
    st.subheader("Carta não está na lista?")
    with st.expander("Adicionar Manualmente"):
        m_nome = st.text_input("Nome da carta")
        m_cor = st.selectbox("Cor", ["Branco", "Azul", "Preto", "Vermelho", "Verde", "Multicolor", "Incolor"])
        m_cmc = st.number_input("CMC", 0, 10, 2)
        m_tier = st.select_slider("Tier", ["S", "A", "B", "C", "D"], value="C")
        if st.button("Adicionar Manual ✅"):
            st.session_state.pool.append({"nome": m_nome, "cor": m_cor, "cmc": m_cmc, "tier": m_tier, "faculdade": "Manual"})
            st.success("Adicionada!")

# --- AREA DE ANÁLISE ---
if st.session_state.pool:
    df_pool = pd.DataFrame(st.session_state.pool)
    
    st.divider()
    st.header("2. Análise do Deck")
    
    c1, c2 = st.columns()
    
    with c1:
        st.subheader("Sua Pool Atual")
        st.dataframe(df_pool, use_container_width=True)
        if st.button("🗑️ Limpar Pool"):
            st.session_state.pool = []
            st.rerun()

    with c2:
        st.subheader("Curva de Mana")
        fig, ax = plt.subplots()
        df_pool['cmc'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#4e008e')
        st.pyplot(fig)

    # --- IA: GERADOR DE DECK ---
    st.divider()
    if st.button("🪄 IA: GERAR DECK DE 40 CARTAS"):
        if len(df_pool) < 10:
            st.warning("Adicione pelo menos 10 cartas para a IA sugerir uma base.")
        else:
            # Lógica: Seleciona as 23 melhores cartas por Tier
            tier_rank = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4}
            df_pool['rank'] = df_pool['tier'].map(tier_rank)
            deck = df_pool.sort_values(by=['rank', 'cmc']).head(23)
            
            st.subheader("📋 Sugestão da IA (23 Mágicas)")
            st.table(deck[['nome', 'cor', 'cmc', 'tier']])
            st.info("💡 Complete com 17 terrenos (total 40 cartas).")
