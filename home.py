import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide', page_title="Detran App")

st.markdown("""
            <div id="main">
            <h1 style="text-align: left; color: rgb(61, 5, 5); font-family: "Gill Sans", sans-serif;">Dataset do Detran (2007 - 2025)</h1>
            <h4 style="text-align: left; font-family: "Gill Sans", sans-serif;">Projeto desenvolvido com o banco de dados disponibilizado no site do Detran dos anos 2007 a 2025. São 3 páginas para análise de dados separadas pelo tipo de classificação. Na sidebar de cada página, conta com um seletor de ano, tornando o gráfico dinâmico.</h4>
            <br>                                                                                                                        
            <h4 style="color: rgb(67, 2, 2); font-family: "Gill Sans", sans-serif;">acidentes por municipio: </h4>
            <h5 style="font-family: "Gill Sans", sans-serif;">Conta com um gráfico de barras horizontais apenas para os 20 primeiros municípíos com mais acidentes</h5>
            <br>
            <h4 style="color: rgb(67, 2, 2); font-family: "Gill Sans", sans-serif;">classificacoes: </h4>
            <h5 style="font-family: "Gill Sans", sans-serif;">São cinco gráficos representando alguns tipos disponíveis de classificação. 2 gráficos de pizza para a classificação dos acidentes, se foi sem ou com vítimas e com o tipo de acidente, por exemplo, uma colisão traseira. 1 gráfico de linha comparando os acidentes com a condição meteorológica. 1 gráfico de barra vertical mostrando os tipos de pistas (simples e dupla). E 1 gráfico de treemap, com - até - as 20 causas de acidentes mais comuns.</h5>
            <br>
            <h4 style="color: rgb(67, 2, 2); font-family: "Gill Sans", sans-serif;">dia mes e ano: </h4>
            <h5 style="font-family: "Gill Sans", sans-serif;">Apresentando 3 gráficos de barras horizontais, para questões como: número de acidentes pelo dia da semana, pelo horário e pela data. Com um botão para filtrar se deseja o menor ou maior número de acidentes.</h5>
            <br>
            <h2><a style="text-decoration: None; color: rgb(124, 20, 20)"href="https://github.com/HugoCDM/" target="_blank">Perfil no GitHub</a></h2>
            </div>
<style>
    #main{
            border: 2px solid rgb(122, 1, 1);
            border-radius: 40px;
            padding: 20px; 
            margin-top: 10px;}

</style>

""", unsafe_allow_html=True)
