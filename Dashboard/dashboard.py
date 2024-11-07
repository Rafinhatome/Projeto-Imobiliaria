import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from millify import millify
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.formula.api import ols


st.title('Imoveis em Blumenau')


# Buscando os dados
dados_imoveis_raw = pd.read_csv(
    r'C:\Users\Rafael Tomé\OneDrive\Área de Trabalho\Analises\Portifólio de projetos\Projeto Imobiliaria\imoveis_limpo.csv')

# Filtro de bairro
bairros = ['Blumenau', 'Escola Agrícola', 'Velha', 'Victor Konder', 'Salto Weissbach',
           'Valparaiso', 'Água Verde', 'Itoupava Seca', 'Fortaleza', 'Centro',
           'Salto', 'Itoupava Central', 'Jardim Blumenau', 'Itoupavazinha',
           'Itoupava Norte', 'Vila Nova', 'Vorstadt', 'Velha Central',
           'Salto Norte', 'Fortaleza Alta', 'Boa Vista', 'Ponta Aguda',
           'Vila Formosa', 'Fidelis', 'Progresso', 'Ribeirão Fresco',
           'Garcia', 'Testo Salto', 'Velha Grande', 'Passo Manso', 'Tribess',
           'Nova Esperança', 'Belchior Central', 'Badenfurt', 'Bom Retiro',
           'Glória', 'Vila Itoupava']

# Filtro de tipo de imovel
tipo_imovel = ['Todos', 'Casa', 'Apartamento']

# Filtros side bar:
st.sidebar.title('Filtros')
bairro = st.sidebar.selectbox('Bairros', bairros)

# Se o bairro for "Blumenau", considera todos os bairros
if bairro == 'Blumenau':
    bairro = ''

tipo = st.sidebar.selectbox('Tipo de imovéis', tipo_imovel)

# Se o tipo for "Todos", considera todos os tipos
if tipo == 'Todos':
    tipo = ''

# Aplicando filtros
dados_imoveis = dados_imoveis_raw
if bairro:
    dados_imoveis = dados_imoveis[dados_imoveis["Bairros"] == bairro]
if tipo:
    dados_imoveis = dados_imoveis[dados_imoveis["Tipo"] == tipo]


# Valores Geral

prefixes = [' mil', ' milhões', ' bilhões']
valores_geral = dados_imoveis['Valores'].sum()
valores_geral = millify(valores_geral, precision=3, prefixes=prefixes)


# Quantidade Geral

quantidade_geral = dados_imoveis.shape[0]
quantidade_geral = millify(quantidade_geral, precision=3, prefixes=prefixes)

# valor mtr² Geral

valor_mtr = (dados_imoveis['Valores'] / dados_imoveis['Tamanho']).mean()
valor_mtr = millify(valor_mtr, precision=3, prefixes=prefixes)


# Casas a venda por bairro:
casas_venda_bairro = dados_imoveis.groupby('Bairros').size()
casas_venda_bairro_ordenados = casas_venda_bairro.sort_values(ascending=False)
top_10 = casas_venda_bairro_ordenados

# Gráfico de top 10 bairros (está todos os valores)

fig_top_10 = plt.figure(figsize=(10, 8))
ax = sns.barplot(x=top_10.values, y=top_10.index)

ax.set_title('Quantidade de Casas à Venda por Bairro\n',
             fontsize=18, loc='left')
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticklabels([])
ax.yaxis.set_tick_params(labelsize=10)
sns.despine(left=True, bottom=True)

for i, valor in enumerate(top_10.values):
    ax.text(valor, i, f'{valor}', va='center', fontsize=10,
            fontweight='bold', ha='right', color='white')


# Top 10 bairros por valor a venda
bairros_valor = dados_imoveis.groupby('Bairros')['Valores'].sum('Valor')
bairros_valor_ordenados = bairros_valor.sort_values(ascending=False)
top_10_bairros_valor = bairros_valor_ordenados

# Gráfico Top 10 bairros por valor a venda (está todos os valores)

fig_valor_Top_10 = plt.figure(figsize=(15, 10))
ax = sns.barplot(x=top_10_bairros_valor.values, y=top_10_bairros_valor.index)

ax.set_title('Valor total de Casas à Venda por Bairro\n',
             fontsize=18, loc='left')
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticklabels([])
ax.yaxis.set_tick_params(labelsize=10)
sns.despine(left=True, bottom=True)

for i, valor in enumerate(top_10_bairros_valor.values):
    qtd = f'R$ {valor:,.2f}'.replace(',', '.')
    offset = 1e3  # offset de 1.000
    ax.text(valor - offset, i, qtd, color='white', fontsize=10,
            fontweight='bold', ha='right', va='center')


#  Valor Médio
# Mantendo a média numérica e ordenando
bairros_media = dados_imoveis[['Bairros', 'Valores']]
media_por_bairro = bairros_media.groupby('Bairros')['Valores'].mean()

# Ordenando pelos valores médios numéricos
media_por_bairro_ordenada = media_por_bairro.sort_values(ascending=False)

# Gráfico de top 10 bairros

fig_top_valor_medio = plt.figure(figsize=(10, 8))
ax = sns.barplot(x=media_por_bairro_ordenada,
                 y=media_por_bairro_ordenada.index)

ax.set_title('Valor médio de Casas à Venda por Bairro\n',
             fontsize=18, loc='left')
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticklabels([])
ax.yaxis.set_tick_params(labelsize=10)
sns.despine(left=True, bottom=True)

for i, valor in enumerate(media_por_bairro_ordenada):
    qtd = f'R$ {valor:,.2f}'.replace(',', '.')
    offset = 1e3  # offset de 1.000
    ax.text(valor - offset, i, qtd, color='white', fontsize=10,
            fontweight='bold', ha='right', va='center')


# preço médio por mtr²

dados_imoveis['Preço por mtr²'] = (
    dados_imoveis['Valores'] / dados_imoveis['Tamanho']).round(2)
preco_medio_mtr = dados_imoveis.groupby(
    'Bairros')[['Valores', 'Preço por mtr²']].mean().round(2)
preco_medio_mtr = preco_medio_mtr.sort_values(
    'Preço por mtr²', ascending=False)

# Selecionando a coluna de valores médios para exibição
preco_mtr = preco_medio_mtr['Preço por mtr²']

fig_preco_mtr = plt.figure(figsize=(10, 8))
ax = sns.barplot(x=preco_mtr, y=preco_medio_mtr.index)

ax.set_title('Valor médio mtr² à Venda por Bairro\n', fontsize=18, loc='left')
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticklabels([])  # Remover labels do eixo x
ax.yaxis.set_tick_params(labelsize=10)
sns.despine(left=True, bottom=True)

# Adicionando os valores formatados no gráfico
for i, valor in enumerate(preco_mtr):
    qtd = f'R$ {valor:,.2f}'.replace(',', '.')  # Formatar o valor
    offset = 1e3  # Offset de 1.000
    ax.text(valor - offset, i, qtd, color='white', fontsize=10,
            fontweight='bold', ha='right', va='center')


aba1, aba2, aba3, aba4 = st.tabs(
    ['Precificação', 'Quantidade de imoveis', 'Valor de imoveis', 'Valor por mtr²'])


with aba1:
    # Criando os dois contêineres
    container1 = st.container()
    container2 = st.container()

    # Primeiro contêiner (com 3 colunas)
    with container1:
        # Definindo as 3 colunas com espaçamento pequeno
        coluna1, coluna2, coluna3 = st.columns(3, gap='small')
        with coluna1:
            st.metric('Valores', valores_geral)
        with coluna2:
            st.metric('Quantidade de imóveis', quantidade_geral)
        with coluna3:
            st.metric('Valor por m²', valor_mtr)

    # Segundo contêiner (com inputs de números)
    with container2:
        const = 1
        suites = st.number_input(
            "Quantidade de suites do imóvel", min_value=1, step=1)
        quartos = st.number_input(
            "Quantidade de quartos do imóvel", min_value=1, step=1)
        vagas = st.number_input(
            "Quantidade de vagas do imóvel", min_value=0, step=1)
        tamanho = st.number_input(
            "Tamanho do imóvel (em m²)", min_value=10, step=10)

# Modelo de precificação de imóveis

dados_casas = dados_imoveis[[
    'Suítes', 'Quartos', 'Vagas', 'Tamanho', 'Valores']]

# Definindo y e X
y = dados_casas['Valores']
X = dados_casas.drop(columns='Valores')

# Aplicando o split do y e X
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Dados de treino para usar na fórmula
df_train = pd.DataFrame(data=X_train)
df_train['Valores'] = y_train

# Ajustando o primeiro modelo com fórmula
modelo_0 = ols('Valores ~ Tamanho', data=df_train).fit()

# Criando o modelo de regressão (sem fórmula)
X_train = sm.add_constant(X_train)  # Adicionando constante
modelo_1 = sm.OLS(
    y_train, X_train[['const', 'Suítes', 'Quartos', 'Vagas', 'Tamanho']]).fit()

# Prevendo com o modelo
X_test = sm.add_constant(X_test)  # Adicionando constante no teste
predict_1 = modelo_1.predict(
    X_test[['const', 'Suítes', 'Quartos', 'Vagas', 'Tamanho']])

# Novo imóvel: previsões para o novo imóvel inserido pelo usuário
novo_imovel = pd.DataFrame({
    'const': [const],  # Termo constante (intercepto)
    'Suítes': [suites],
    'Quartos': [quartos],
    'Vagas': [vagas],
    'Tamanho': [tamanho]
})

# Prevendo o valor do novo imóvel
previsao_novo_imovel = modelo_1.predict(
    novo_imovel[['const', 'Suítes', 'Quartos', 'Vagas', 'Tamanho']])

# Exibindo a previsão
st.subheader("Previsão do Valor do Imóvel")
st.write(
    f"O valor estimado para o imóvel com {suites} suite(s), {quartos} quarto(s), {vagas} vaga(s) e {tamanho} m² é: R$ {previsao_novo_imovel[0]:,.2f}")


with aba2:
    container = st.container()
    with container:
        coluna1, coluna2, coluna3 = st.columns(3, gap='small')
        with coluna1:
            st.metric('Valores', valores_geral)
        with coluna2:
            st.metric('Quantidade de imoveis', quantidade_geral)
        with coluna3:
            st.metric('Valor por mtr²', valor_mtr)
    st.pyplot(fig_top_10, use_container_width=True,)


with aba3:
    container = st.container()
    with container:
        coluna1, coluna2, coluna3 = st.columns(3, gap='small')
        with coluna1:
            st.metric('Valores', valores_geral)
        with coluna2:
            st.metric('Quantidade de imoveis', quantidade_geral)
        with coluna3:
            st.metric('Valor por mtr²', valor_mtr)
    st.pyplot(fig_top_valor_medio, use_container_width=True)


with aba4:
    container = st.container()
    with container:
        coluna1, coluna2, coluna3 = st.columns(3, gap='small')
        with coluna1:
            st.metric('Valores', valores_geral)
        with coluna2:
            st.metric('Quantidade de imoveis', quantidade_geral)
        with coluna3:
            st.metric('Valor por mtr²', valor_mtr)
    st.pyplot(fig_preco_mtr, use_container_width=True)
