import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000/chat"

# Listar chats
def listar_chats(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/chats", headers=headers)
    return response.json().get("chats", [])

# Criar chat
def criar_chat(token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"titulo": "Novo Chat"}
    response = requests.post(f"{API_URL}/chats", json=data, headers=headers)

    if response.status_code == 201:
        return response.json()["chat_id"]
    return None

# Excluir chat
def excluir_chat(token, chat_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/chats/{chat_id}", headers=headers)
    return response.status_code == 200

# Criar menu lateral
def menu_lateral():
    st.sidebar.title("📌 Chats")
    token = st.session_state.get("token", None)

    if token:
        chats = listar_chats(token)

        for chat in chats:
            if st.sidebar.button(chat["titulo"]):
                st.session_state["chat_id"] = chat["idchat"]
                st.rerun()

        if st.sidebar.button("➕ Novo Chat"):
            chat_id = criar_chat(token)
            if chat_id:
                st.session_state["chat_id"] = chat_id
                st.rerun()

        if st.sidebar.button("❌ Excluir Chat"):
            if "chat_id" in st.session_state:
                excluir_chat(token, st.session_state["chat_id"])
                del st.session_state["chat_id"]
                st.rerun()

