import requests
import streamlit as st
from sidebar import menu_lateral
from auth import API_URL

# Função para enviar mensagem ao backend
def enviar_mensagem(token, chat_id, mensagem):
    headers = {"Authorization": f"Bearer {token}"}
    url = "http://127.0.0.1:5000/mensagem/mensagens"
    data = {"idchat": chat_id, "conteudo": mensagem}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return response.json()["resposta"]  # Retorna a resposta da LLM
    return "Erro ao obter resposta."

# Página principal do chat
def chat_page():
    st.title("💬 Chat com LLM")

    # Recuperar token e usuário
    if "token" not in st.session_state:
        st.warning("Você precisa fazer login para acessar o chat!")
        st.stop()

    token = st.session_state["token"]
    chat_id = st.session_state.get("chat_id", None)

    if not chat_id:
        st.info("Selecione ou crie um chat no menu lateral.")
        st.stop()

    # Exibir histórico do chat
    st.subheader(f"Chat {chat_id}")

    if "mensagens" not in st.session_state:
        st.session_state["mensagens"] = []

    for msg in st.session_state["mensagens"]:
        with st.chat_message(msg["origem"]):
            st.write(msg["conteudo"])

    # Entrada de texto
    mensagem = st.chat_input("Digite sua mensagem...")

    if mensagem:
        st.session_state["mensagens"].append({"origem": "usuario", "conteudo": mensagem})
        with st.chat_message("usuario"):
            st.write(mensagem)

        resposta = enviar_mensagem(token, chat_id, mensagem)

        st.session_state["mensagens"].append({"origem": "LLM", "conteudo": resposta})
        with st.chat_message("LLM"):
            st.write(resposta)