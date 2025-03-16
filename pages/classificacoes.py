import pandas as pd
import plotly.express as px
import os
import streamlit as st


def formatar_graficos(grafico, legenda=''):
    if legenda:
        grafico.update_layout(
            xaxis_title='', yaxis_title='', title=dict(font={'size': 25}), legend_title_font={'size': 18}, legend={'font': {'size': 18}}, legend_title_text=(legenda))
    else:
        grafico.update_layout(
            xaxis_title='', yaxis_title='', title=dict(font={'size': 25}), legend_title_font={'size': 18}, legend={'font': {'size': 18}})

    grafico.update_traces(textfont=dict(size=18))
    grafico.update_yaxes(tickfont=dict(size=18))
    grafico.update_xaxes(tickfont=dict(size=18))


detran_anos = []

files = os.listdir('detran_year')
for file in files:
    if file.endswith('.csv'):
        detran_anos.append(file.replace(
            'datatran', '').replace('.csv', ''))
detran_anos = sorted(detran_anos)

st.set_page_config(layout='wide')
st.markdown('''
<style>

.st-emotion-cache-0 {
        margin-top: -20px;
    }

  
div[data-testid="stMarkdownContainer"]{
        font-size: 18px;

            }
div[data-baseweb="select"] {
        margin-left: -4px;   }
</style>''', unsafe_allow_html=True)
col1, col2 = st.columns((1.5, 2.5))
con1 = col1.container(border=True)
con2 = col2.container(border=True)
con3 = st.container(border=True)
con4 = st.container(border=True)


@st.cache_data
def reader(ano):
    df = pd.read_csv(
        f'./detran_year/datatran{ano}.csv', encoding='ISO-8859-1', sep=';')

    return df


ano = st.sidebar.selectbox('Selecione o ano', options=detran_anos)
df = reader(ano)

classificacao_por_tipo_acidente_colunas = df['classificacao_acidente'].value_counts(
).reset_index(name='qtd')
classificacao_por_tipo_acidente_colunas = classificacao_por_tipo_acidente_colunas[
    classificacao_por_tipo_acidente_colunas['classificacao_acidente'].isin(['Sem Vítimas', 'Com Vítimas Feridas', 'Com Vítimas Fatais'])]


frequencia_classificacao_acidente = px.pie(classificacao_por_tipo_acidente_colunas, names='classificacao_acidente',
                                           values='qtd', title=f"Gráfico de Classificação de acidentes - {ano}", height=400)

df = df[df['tipo_pista'].isin(['Simples', 'Dupla'])]

df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S')

df['horario'] = df['horario'].dt.hour

horario_tipo_pista = df.groupby(
    ['horario', 'tipo_pista']).size().reset_index(name='quantidade')
horario_tipo_pista_bar = px.bar(horario_tipo_pista, x='horario', y='quantidade', color='tipo_pista',
                                barmode='group', text_auto=True, title=f'Gráfico dos tipos de pistas pelos Horários e Quantidade - {ano}', height=750)


frequencia_acidentes = df['tipo_acidente_frequencia'] = (
    df['tipo_acidente'].value_counts(normalize=True) * 100).round(2)

soma_acidentes = df['tipo_acidente'].value_counts()

df_frequencia = pd.DataFrame({
    'frequencia_acidentes': frequencia_acidentes,
    'soma_acidentes': soma_acidentes
})

attr_mudado = df['tipo_acidente'].value_counts()
attr_mudado = attr_mudado.iloc[0:5]


grafico = px.pie(attr_mudado, names=attr_mudado.index, values=attr_mudado.values,
                 title=f'Gráfico dos Tipos de acidente - {ano}', height=420)


meteorologia_e_classificacao = df.groupby('condicao_metereologica')[
    'classificacao_acidente'].value_counts().reset_index(name='quantidade_acidentes')
meteorologia_e_classificacao = meteorologia_e_classificacao.replace(
    '(null)', 'Indefinido')
meteorologia_e_classificacao = meteorologia_e_classificacao[meteorologia_e_classificacao['classificacao_acidente'].isin(
    ['Com Vítimas Feridas', 'Sem Vítimas', 'Com Vítimas Fatais'])]
meteorologia_e_classificacao_line = px.line(meteorologia_e_classificacao, x='condicao_metereologica', y='quantidade_acidentes',
                                            color='classificacao_acidente',  title=f'Gráfico da Condição Meteorológica pela Classificação e Quantidade de acidentes - {ano}', height=836)
meteorologia_e_classificacao_line.update_layout(legend=dict(title=None))
#
#
#
##
##

acidentes_fatais_causas_mortes = df[[
    'causa_acidente', 'classificacao_acidente', 'mortos']]
acidentes_fatais_causas_mortes = acidentes_fatais_causas_mortes.dropna()

acidentes_fatais_causas_mortes = acidentes_fatais_causas_mortes[
    acidentes_fatais_causas_mortes['classificacao_acidente'] == 'Com Vítimas Fatais']
acidentes_fatais_causas_mortes_agrupado = acidentes_fatais_causas_mortes.groupby(
    ['classificacao_acidente', 'causa_acidente'])['mortos'].sum().reset_index().sort_values(by='mortos')

acidentes_fatais_causas_mortes_agrupado_treemap = px.treemap(acidentes_fatais_causas_mortes_agrupado.iloc[:25], path=[
                                                             'causa_acidente'], values='mortos', color_continuous_scale='Blues', color='mortos', title='Distribuição das Causas de Acidentes Fatais e o Número de Mortes')
acidentes_fatais_causas_mortes_agrupado_treemap.update_traces(
    marker=dict(cornerradius=15))
acidentes_fatais_causas_mortes_agrupado_treemap.update_layout(
    coloraxis_colorbar=dict(title='Mortos', title_font={'size': 18}, tickfont={'size': 18}))

formatar_graficos(frequencia_classificacao_acidente)
formatar_graficos(horario_tipo_pista_bar, 'Tipo de pista')
formatar_graficos(grafico)
formatar_graficos(meteorologia_e_classificacao_line)
formatar_graficos(acidentes_fatais_causas_mortes_agrupado_treemap)

con1.plotly_chart(frequencia_classificacao_acidente)
con1.plotly_chart(grafico)
con2.plotly_chart(meteorologia_e_classificacao_line)


con3.plotly_chart(horario_tipo_pista_bar)
con4.plotly_chart(acidentes_fatais_causas_mortes_agrupado_treemap)
