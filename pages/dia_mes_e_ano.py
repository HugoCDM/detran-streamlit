import pandas as pd
import plotly.express as px
import os
import streamlit as st
from datetime import datetime


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
col1, col2 = st.columns(2)
con1 = col1.container(border=True)
con2 = col2.container(border=True)
con3 = st.container(border=True)
st.markdown('''
            
<style>

.st-emotion-cache-0 {
        margin-top: -18px;
    }


div[data-testid="stMarkdownContainer"]{
        font-size: 18px;

            }
div[data-baseweb="select"] {
        margin-left: -4px;   }
            

</style>''', unsafe_allow_html=True)


@st.cache_data
def reader(ano):
    df = pd.read_csv(
        f'./detran_year/datatran{ano}.csv', encoding='latin-1', sep=';', low_memory=False)

    df['dia_semana'] = df['dia_semana'].apply(
        lambda x: x.title().replace('-Feira', ''))
    df['data_inversa'] = df['data_inversa'].apply(lambda x: datetime.strptime(
        x, '%Y-%m-%d').strftime('%d/%m/%Y') if '-' in x else x)

    return df


def maior_menor_graficos(ano, ascending, maior_menor):

    acidentes_no_dia_da_semana = df['dia_semana'].value_counts(
    ).reset_index(name='qtd').sort_values(by='qtd', ascending=ascending)

    acidentes_no_dia_da_semana_bar = px.bar(
        acidentes_no_dia_da_semana, orientation='h', x='qtd', y='dia_semana', color='dia_semana', text_auto=True, title=f'{maior_menor} número de acidentes pelo dia da semana - {ano}', height=375)
    acidentes_no_dia_da_semana_bar.update_layout(
        xaxis={'tickformat': '.0f'})

    formatar_graficos(acidentes_no_dia_da_semana_bar, 'Dia da semana')
    con1.plotly_chart(acidentes_no_dia_da_semana_bar)

    acidentes_pela_data_completa = df['data_inversa'].value_counts(
    ).reset_index(name='qtd').sort_values(by='qtd', ascending=ascending).iloc[:7]

    acidentes_pela_data_completa_bar = px.bar(
        acidentes_pela_data_completa, orientation='h', x='qtd', y='data_inversa', color='data_inversa', text_auto=True, title=f'{maior_menor} número de acidentes pela data completa - {ano}', height=375)
    formatar_graficos(acidentes_pela_data_completa_bar, 'Data')
    con2.plotly_chart(acidentes_pela_data_completa_bar)

    df['horario'] = df['horario'].str[0:2]
    acidentes_pelo_horario = df.groupby('horario').size(
    ).reset_index(name='qtd')
    acidentes_pelo_horario = acidentes_pelo_horario.sort_values(
        by='qtd', ascending=ascending)
    acidentes_pelo_horario_bar = px.bar(
        acidentes_pelo_horario.iloc[0:7], x='qtd', y='horario', orientation='h', color='horario', text_auto=True, title=f'{maior_menor} número de acidentes pelo horário - {ano}', height=423)

    acidentes_pelo_horario_bar.update_layout(
        yaxis=dict(
            type="category"  # Força o eixo Y a tratar os horários corretamente
        ), xaxis={'tickformat': '.0f'}
    )

    formatar_graficos(acidentes_pelo_horario_bar, 'Horário')

    con3.plotly_chart(acidentes_pelo_horario_bar)


ano = st.sidebar.selectbox('Selecione o ano', options=detran_anos)
df = reader(ano)

acidentes = st.sidebar.radio('Gráfico', options=[
    '***:rainbow[Menor número de acidentes]***', '***:rainbow[Maior número de acidentes]***'], label_visibility='hidden')


if acidentes == '***:rainbow[Maior número de acidentes]***':
    maior_menor_graficos(ano, False, 'Maior')

else:
    maior_menor_graficos(ano, True, 'Menor')
