Aqui está a solução completa, estruturada de forma limpa e modular. Seguindo a filosofia de Vibe Coding, o código é enxuto, legível e aproveita os componentes nativos do Streamlit para manter a aplicação leve e rápida.

1. Código Completo: app.py
Python
import pandas as pd
import streamlit as st


# Configuração inicial da página
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Base de Dados Simulada
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    dados = [
        {
            "Item": "Resina Epóxi e Pigmentos",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 4500.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Chapas de Aço Galv.",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 3200.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Programador CNC",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 6500.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Técnico de Montagem",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 4000.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Frete Rodoviário SP-RJ",
            "Categoria": "Logística",
            "Valor (R$)": 2800.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Embalagens Protegidas",
            "Categoria": "Logística",
            "Valor (R$)": 1200.00,
            "Prioridade": "Baixa",
        },
        {
            "Item": "Consumo Maquinário Trifásico",
            "Categoria": "Energia",
            "Valor (R$)": 2100.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Iluminação de Galpão",
            "Categoria": "Energia",
            "Valor (R$)": 950.00,
            "Prioridade": "Baixa",
        },
        {
            "Item": "Brocas e Fresas de Precisão",
            "Categoria": "Ferramentas",
            "Valor (R$)": 1750.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Kit Instrumentos de Medição",
            "Categoria": "Ferramentas",
            "Valor (R$)": 890.00,
            "Prioridade": "Baixa",
        },
    ]
    return pd.DataFrame(dados)


df_base = carregar_dados()

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar) - Filtros e Controles
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Painel de Controle")

# 1. Slider de Orçamento
orcamento_total = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
    format="R$ %.2f",
)

# 2. Multiselect de Categorias
categorias_disponiveis = df_base["Categoria"].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    label="Filtrar por Categorias:",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# Aplicar o filtro no DataFrame
df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]

# -----------------------------------------------------------------------------
# Área Principal
# -----------------------------------------------------------------------------
st.title("💰 Simulador de Custos e Orçamento")
st.markdown("Acompanhe e simule o impacto financeiro das etapas do seu projeto.")

# Cálculos para os cartões
gasto_total = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_total

# 1. Painel de Métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Orçamento Definido",
    value=f"R$ {orcamento_total:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

col2.metric(
    label="Gasto Filtrado",
    value=f"R$ {gasto_total:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

col3.metric(
    label="Saldo Restante",
    value=f"R$ {saldo_restante:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
    delta=f"R$ {saldo_restante:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
    delta_color="normal",
)

st.divider()

# 2. Alerta Visual Condicional
if gasto_total <= orcamento_total:
    st.success(
        f"✅ **Projeto dentro da meta!** Você ainda possui **R$ {saldo_restante:,.2f}** disponíveis."
    )
else:
    excedente = abs(saldo_restante)
    st.error(
        f"⚠️ **Atenção! Orçamento Estourado!** Os custos selecionados ultrapassam o limite em **R$ {excedente:,.2f}**."
    )

st.divider()

# 3. Gráfico Sem Dependências Externas (st.bar_chart)
st.subheader("📊 Distribuição de Custos por Categoria")

if not df_filtrado.empty:
    # Agrupa valores por Categoria para gráfico de barras horizontais nativo
    custos_por_categoria = (
        df_filtrado.groupby("Categoria")["Valor (R$)"]
        .sum()
        .sort_values(ascending=True)
    )

    st.bar_chart(custos_por_categoria, horizontal=True, color="#2b5c8f")
else:
    st.info("Nenhuma categoria selecionada para exibir o gráfico.")

st.divider()

# 4. Tabela de Detalhamento
st.subheader("📋 Itens do Orçamento")

if not df_filtrado.empty:
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Valor (R$)": st.column_config.NumberColumn(
                "Valor", format="R$ %.2f"
            ),
            "Prioridade": st.column_config.SelectboxColumn(
                "Prioridade", options=["Alta", "Média", "Baixa"]
            ),
        },
    )
else:
    st.warning("Nenhum item disponível com as categorias selecionadas.")
