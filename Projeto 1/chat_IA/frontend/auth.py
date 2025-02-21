import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000/auth"  # URL do backend

# Função para autenticar o usuário
def login(email, senha):
    url = f"{API_URL}/login"
    data = {"email": email, "senha": senha}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json() #retorna o token jwt e os dados do usuário
    else:
        return None

# Função para registrar usuário
def register(nome, email, senha):
    url = f"{API_URL}/register"
    data = {"nome": nome, "email": email, "senha": senha}
    response = requests.post(url, json=data)

    return response.json()