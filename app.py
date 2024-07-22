import streamlit as st
from bot.instagram_bot import InstagramBot, save_followers_to_json
import os
import json
import subprocess

def run_bot(username, password):
    bot = InstagramBot(username=username, password=password)
    bot.login()
    
    followers_data = bot.get_followers()
    bot.quit()
    
    return followers_data

def load_followers_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

st.title("Instagram Bot - Coletor de Seguidores")

st.sidebar.header("Credenciais do Instagram")
username = st.sidebar.text_input("Usuário do Instagram")
password = st.sidebar.text_input("Senha do Instagram", type="password")


if st.sidebar.button("Iniciar Bot"):
    if username and password:
        followers_data = run_bot(username, password)
        
        # Salvar os dados em um arquivo JSON
        save_followers_to_json(followers_data, 'data/followers.json')
        
        # Executar o script para processar os seguidores
        subprocess.run(['python', 'data/process_followers.py'])
        
        # Carregar e exibir os seguidores processados
        if os.path.exists('data/followers_processed.json'):
            processed_followers = load_followers_from_json('data/followers_processed.json')
            st.write("**Seguidores Processados:**")
            for follower in processed_followers:
                st.write(f"{follower}")
        else:
            st.error("Erro ao processar seguidores.")
    else:
        st.error("Por favor, insira as credenciais do Instagram.")
