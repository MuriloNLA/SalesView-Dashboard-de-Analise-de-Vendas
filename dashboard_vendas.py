# dashboard_vendas.py
# Dashboard de vendas por representante e regiao.
# Le dados de uma planilha Excel e exibe tabelas e graficos interativos.
#
# Dependencias:
#     pip install pandas streamlit matplotlib openpyxl
#
# Uso:
#     streamlit run dashboard_vendas.py
 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
 
 
# ---------------------------------------------------------------------------
# CONFIGURACAO
# ---------------------------------------------------------------------------
 
ARQUIVO_EXCEL  = "Pedido de Vendas - Logistica V2.xlsx"
ABA_EXCEL      = "Pedidos de venda"
FILTRO_NEGOCIO = "EQ. EXTERNA"
LOGO           = "Logo.png"
 
# ---------------------------------------------------------------------------
 
 
# ---------------------------------------------------------------------------
# FORMATACAO
# ---------------------------------------------------------------------------
 
def formatar_kg(num):
    inteiro, decimal = f"{num:.2f}".split(".")
    inteiro_com_ponto = "{:,}".format(int(inteiro)).replace(",", ".")
    return f"{inteiro_com_ponto},{decimal}"
 
 
def formatar_ton(num_kg):
    toneladas = num_kg / 1000
    inteiro, decimal = f"{toneladas:.2f}".split(".")
    inteiro_com_ponto = "{:,}".format(int(inteiro)).replace(",", ".")
    return f"{inteiro_com_ponto},{decimal}"
 
 
# ---------------------------------------------------------------------------
# DADOS
# ---------------------------------------------------------------------------
 
@st.cache_data
def carregar_dados():
    usecols = ['Data Pedido', 'Qtde Kg', 'Qtde Real', 'Representante Master', 'Região', 'Und. Negócio']
    df = pd.read_excel(ARQUIVO_EXCEL, usecols=usecols, sheet_name=ABA_EXCEL)
    df = df[df['Und. Negócio'] == FILTRO_NEGOCIO]
    df['Ano']      = pd.to_datetime(df['Data Pedido']).dt.year
    df['Mes']      = pd.to_datetime(df['Data Pedido']).dt.month
    df['Semestre'] = df['Mes'].apply(lambda x: '1 Semestre' if x <= 6 else '2 Semestre')
    return df
 
 
# ---------------------------------------------------------------------------
# COMPONENTES
# ---------------------------------------------------------------------------
 
def exibir_tabela_formatada(df, titulo="", renomear_colunas=None, colunas_numericas=None):
    st.subheader(titulo)
 
    if renomear_colunas:
        df = df.rename(columns=renomear_colunas)
 
    estilo = df.style
 
    if colunas_numericas:
        formato = {}
        for col in colunas_numericas:
            if col in df.columns:
                if df[col].dtype in ['int64', 'int32']:
                    formato[col] = '{:,.0f}'.format
                else:
                    formato[col] = lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        estilo = estilo.format(formato)
 
    st.dataframe(estilo)
 
 
# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
 
try:
    st.sidebar.image(LOGO, use_container_width=True)
except Exception:
    pass
 
if st.sidebar.button("Atualizar dados"):
    with st.spinner("Carregando dados..."):
        st.cache_data.clear()
        st.rerun()
 
st.sidebar.title("Filtro por Ano")
ano_selecionado = st.sidebar.selectbox("Selecione o ano:", [2024, 2025, "Todos"])
 
st.sidebar.title("Filtro por Semestre")
semestre_selecionado = st.sidebar.selectbox("Selecione o Semestre", ["1 Semestre", "2 Semestre", "Todos"])
 
 
# ---------------------------------------------------------------------------
# PROCESSAMENTO
# ---------------------------------------------------------------------------
 
planilha = carregar_dados()
 
if semestre_selecionado != "Todos":
    planilha = planilha[planilha['Semestre'] == semestre_selecionado]
 
if ano_selecionado != "Todos":
    planilha = planilha[planilha['Ano'] == ano_selecionado]
 
AgrupadoVendedores = planilha.groupby('Representante Master').agg({
    'Qtde Kg':   ['min', 'mean', 'max', 'sum', 'count'],
    'Qtde Real': ['min', 'mean', 'max', 'sum']
}).reset_index()
 
AgrupadoVendedores.columns = [
    'Representante Master',
    'Minimo vendido', 'Media de vendas em Kg', 'Maximo Vendido', 'Total Kg vendido', 'Quant Vendas',
    'Minimo vendido em volume', 'Media de vendas em volume', 'Maximo Vendido Volume', 'Total Volume vendido'
]
 
AgrupadoRegiao = planilha.groupby('Região').agg({
    'Qtde Kg':   ['min', 'mean', 'max', 'sum', 'count'],
    'Qtde Real': ['min', 'mean', 'max', 'sum']
}).reset_index()
 
AgrupadoRegiao.columns = [
    'Região',
    'Minimo vendido (Kg)', 'Media de Kg', 'Maximo vendido (Kg)', 'Total Kg', 'Total Vendas',
    'Minimo vendido (Qntd Real)', 'Media Volume', 'Maximo vendido (Qntd Real)', 'Total Qntd Real'
]
 
 
# ---------------------------------------------------------------------------
# DASHBOARD — REPRESENTANTE
# ---------------------------------------------------------------------------
 
st.title("Dashboard de Vendas por Representante")
 
exibir_tabela_formatada(
    AgrupadoVendedores[['Representante Master', 'Minimo vendido', 'Media de vendas em Kg', 'Maximo Vendido', 'Total Kg vendido', 'Quant Vendas']],
    titulo="Resumo por Representante (Kg)",
    renomear_colunas={
        'Representante Master': 'Vendedor',
        'Minimo vendido': 'Min (Kg)',
        'Media de vendas em Kg': 'Media (Kg)',
        'Maximo Vendido': 'Max (Kg)',
        'Total Kg vendido': 'Total (Kg)',
        'Quant Vendas': 'Qtd Vendas'
    },
    colunas_numericas=['Min (Kg)', 'Media (Kg)', 'Max (Kg)', 'Total (Kg)', 'Qtd Vendas']
)
 
exibir_tabela_formatada(
    AgrupadoVendedores[['Representante Master', 'Minimo vendido em volume', 'Media de vendas em volume', 'Maximo Vendido Volume', 'Total Volume vendido']],
    titulo="Resumo por Representante (Volume)",
    renomear_colunas={
        'Representante Master': 'Vendedor',
        'Minimo vendido em volume': 'Min (Unid)',
        'Media de vendas em volume': 'Media (Unid)',
        'Maximo Vendido Volume': 'Max (Unid)',
        'Total Volume vendido': 'Total (Unid)'
    },
    colunas_numericas=['Min (Unid)', 'Media (Unid)', 'Max (Unid)', 'Total (Unid)']
)
 
 
# ---------------------------------------------------------------------------
# DASHBOARD — REGIAO
# ---------------------------------------------------------------------------
 
st.title("Dashboard de Vendas por Região")
 
exibir_tabela_formatada(
    AgrupadoRegiao[['Região', 'Minimo vendido (Kg)', 'Media de Kg', 'Maximo vendido (Kg)', 'Total Kg', 'Total Vendas']],
    titulo="Resumo por Região (Kg)",
    renomear_colunas={
        'Minimo vendido (Kg)': 'Min (Kg)',
        'Media de Kg': 'Media (Kg)',
        'Maximo vendido (Kg)': 'Max (Kg)',
        'Total Kg': 'Total (Kg)',
        'Total Vendas': 'Vendas Feitas'
    },
    colunas_numericas=['Min (Kg)', 'Media (Kg)', 'Max (Kg)', 'Total (Kg)', 'Vendas Feitas']
)
 
exibir_tabela_formatada(
    AgrupadoRegiao[['Região', 'Minimo vendido (Qntd Real)', 'Media Volume', 'Maximo vendido (Qntd Real)', 'Total Qntd Real']],
    titulo="Resumo por Região (Volume)",
    renomear_colunas={
        'Minimo vendido (Qntd Real)': 'Min (Volume)',
        'Media Volume': 'Media (Volume)',
        'Maximo vendido (Qntd Real)': 'Max (Volume)',
        'Total Qntd Real': 'Total (Volume)'
    },
    colunas_numericas=['Min (Volume)', 'Media (Volume)', 'Max (Volume)', 'Total (Volume)']
)
 
 
# ---------------------------------------------------------------------------
# TOTAIS GERAIS
# ---------------------------------------------------------------------------
 
total_kg     = planilha['Qtde Kg'].sum()
media_kg     = planilha['Qtde Kg'].mean()
total_volume = planilha['Qtde Real'].sum()
media_volume = planilha['Qtde Real'].mean()
 
st.title("Totais Gerais")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    st.markdown("**Total vendido (Kg)**")
    st.write(f"{formatar_kg(total_kg)} kg")
    st.markdown("**Total Vendido (Toneladas)**")
    st.write(formatar_ton(total_kg))
 
with col2:
    st.markdown("**Media por venda (Kg)**")
    st.write(f"{formatar_kg(media_kg)} kg")
    st.markdown("**Media por venda (Toneladas)**")
    st.write(formatar_ton(media_kg))
 
with col3:
    st.markdown("**Total vendido (Volume)**")
    st.write(f"{formatar_kg(total_volume)} unidades")
    st.markdown("**Media por venda (Volume)**")
    st.write(f"{formatar_kg(media_volume)} unidades")
 
 
# ---------------------------------------------------------------------------
# GRAFICO
# ---------------------------------------------------------------------------
 
st.subheader("Distribuição de Vendas por Região")
 
fig, ax = plt.subplots()
ax.pie(
    AgrupadoRegiao['Total Kg'],
    labels=AgrupadoRegiao['Região'],
    autopct='%1.1f%%',
    startangle=90
)
ax.axis('equal')
st.pyplot(fig)