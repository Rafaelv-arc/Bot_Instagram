import streamlit as st
from bot.instagram_bot import InstagramBot, save_followers_to_json

def run_bot(username, password):
    # Remova o parâmetro use_facebook do construtor
    bot = InstagramBot(username=username, password=password)
    bot.login()
    
    followers_data = bot.get_followers()
    bot.quit()
    
    return followers_data

st.title("Instagram Bot - Coletor de Seguidores")

st.sidebar.header("Credenciais do Instagram")
username = st.sidebar.text_input("Usuário do Instagram")
password = st.sidebar.text_input("Senha do Instagram", type="password")

if st.sidebar.button("Iniciar Bot"):
    if username and password:
        followers_data = run_bot(username, password)
        st.write("**Seguidores Encontrados:**")
        for follower in followers_data:
            st.write(f"Nome: {follower}")
        # Opcional: salvar os dados em um arquivo JSON
        save_followers_to_json(followers_data)
        st.success("Dados dos seguidores salvos com sucesso.")
    else:
        st.error("Por favor, insira as credenciais do Instagram.")
