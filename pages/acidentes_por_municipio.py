import pandas as pd
import plotly.express as px
import os
import streamlit as st


detran_anos = []

files = os.listdir('detran_year')
for file in files:
    if file.endswith('.csv'):
        detran_anos.append(file.replace(
            'datatran', '').replace('.csv', ''))


st.set_page_config(layout='wide')
con1 = st.container()
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

.stVerticalBlockBorderWrapper{
            background-color: blue;}
</style>''', unsafe_allow_html=True)

col1, col2 = st.columns((0.5, 2))


@st.cache_data
def reader(ano):
    df = pd.read_csv(
        f'./detran_year/datatran{ano}.csv', encoding='latin-1', sep=';')

    return df


ano = st.sidebar.selectbox('Selecione o ano', options=detran_anos)


df_accidents_by_municipality = reader(ano)
df_accidents_by_municipality['municipio'] = df_accidents_by_municipality['municipio'].str.title(
)
df_accidents_by_municipality['municipio_uf'] = df_accidents_by_municipality['municipio'] + \
    ' (' + df_accidents_by_municipality['uf'] + ')'
df_accidents_by_municipality = df_accidents_by_municipality['municipio_uf'].value_counts().reset_index(
    name='qtd').sort_values(by='qtd', ascending=False).iloc[0:20]
df_accidents_by_municipality_plot = px.bar(df_accidents_by_municipality, orientation='h', x='qtd', y='municipio_uf', color='municipio_uf',
                                           text_auto=True, height=850, title=f'Municípios com o maior registro de acidentes - {ano}')
df_accidents_by_municipality_plot.update_layout(
    xaxis_title='', yaxis_title='', title=dict(font={'size': 30}), legend_title_font={'size': 20}, legend={'font': {'size': 20}}, legend_title_text=('Municípios'))
df_accidents_by_municipality_plot.update_traces(textfont=dict(size=20))
df_accidents_by_municipality_plot.update_yaxes(tickfont=dict(size=18))
df_accidents_by_municipality_plot.update_xaxes(tickfont=dict(size=18))


con1.plotly_chart(df_accidents_by_municipality_plot)
