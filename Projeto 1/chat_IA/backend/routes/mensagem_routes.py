from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from openai import OpenAI
import os
from dotenv import load_dotenv
from db import get_connection

mensagem_bp = Blueprint('mensagem', __name__)

# ✅ Carregar a chave da OpenAI do .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------
# ✅ Função para buscar dados de todas as tabelas do banco
# ---------------------------
# def obter_dados_do_banco():
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     try:
#         # 🐮 Buscar dados da fazenda
#         cursor.execute("SELECT * FROM fazenda")
#         fazendas = cursor.fetchall()

#         # 📋 Buscar dados dos animais inseminados
#         cursor.execute("SELECT * FROM animal_inseminado")
#         animais = cursor.fetchall()

#         # 🔬 Buscar dados das inseminações
#         cursor.execute("SELECT * FROM inseminacao")
#         inseminacoes = cursor.fetchall()

#         # 🔍 Formatando os dados para o prompt
#         dados_formatados = "\n\n".join([
#             f"🏡 **Fazendas:**\n" + "\n".join([
#                 f"ID: {f['idfazenda']}, Nome: {f['nome']}, Município: {f['municipio']}, Estado: {f['estado']}"
#                 for f in fazendas
#             ]),
#             f"🐂 **Animais Inseminados:**\n" + "\n".join([
#                 f"ID: {a['idanimal_inseminado']}, Número: {a['numero_animal']}, Lote: {a['lote']}, "
#                 f"Raça: {a['raca']}, Categoria: {a['categoria']}, ECC: {a['ECC']}, Ciclicidade: {a['ciclicidade']}"
#                 for a in animais
#             ]),
#             f"🧬 **Protocolos de Inseminação:**\n" + "\n".join([
#                 f"ID: {i['idinseminacao']}, Protocolo: {i['protocolo']}, Touro: {i['touro']}, "
#                 f"Raça do Touro: {i['raca_touro']}, Empresa: {i['empresa_touro']}, "
#                 f"Inseminador: {i['inseminador']}, Nº IATF: {i['numero_IATF']}, DG: {i['DG']}, Perda: {i['perda']}"
#                 for i in inseminacoes
#             ])
#         ])

#         return dados_formatados

#     except Exception as e:
#         print("❌ ERRO AO BUSCAR DADOS DO BANCO:", str(e))
#         return "Não foi possível acessar os dados do banco."

#     finally:
#         cursor.close()
#         conn.close()
def obter_dados_do_banco():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 🐮 Buscar dados da fazenda
        sql_fazenda = "SELECT * FROM fazenda"
        print(f"📌 CONSULTA SQL - FAZENDA: {sql_fazenda}")  # 👀 Ver consulta
        cursor.execute(sql_fazenda)
        fazendas = cursor.fetchall()

        # 📋 Buscar dados dos animais inseminados
        sql_animais = "SELECT * FROM animal_inseminado"
        print(f"📌 CONSULTA SQL - ANIMAIS: {sql_animais}")  # 👀 Ver consulta
        cursor.execute(sql_animais)
        animais = cursor.fetchall()

        # 🔬 Buscar dados das inseminações
        sql_inseminacoes = "SELECT * FROM inseminacao"
        print(f"📌 CONSULTA SQL - INSEMINAÇÕES: {sql_inseminacoes}")  # 👀 Ver consulta
        cursor.execute(sql_inseminacoes)
        inseminacoes = cursor.fetchall()

        # 🔍 Formatando os dados para o prompt
        dados_formatados = "\n\n".join([
            f"🏡 **Fazendas:**\n" + "\n".join([
                f"ID: {f['idfazenda']}, Nome: {f['nome']}, Município: {f['municipio']}, Estado: {f['estado']}"
                for f in fazendas
            ]),
            f"🐂 **Animais Inseminados:**\n" + "\n".join([
                f"ID: {a['idanimal_inseminado']}, Número: {a['numero_animal']}, Lote: {a['lote']}, "
                f"Raça: {a['raca']}, Categoria: {a['categoria']}, ECC: {a['ECC']}, Ciclicidade: {a['ciclicidade']}"
                for a in animais
            ]),
            f"🧬 **Protocolos de Inseminação:**\n" + "\n".join([
                f"ID: {i['idinseminacao']}, Protocolo: {i['protocolo']}, Touro: {i['touro']}, "
                f"Raça do Touro: {i['raca_touro']}, Empresa: {i['empresa_touro']}, "
                f"Inseminador: {i['inseminador']}, Nº IATF: {i['numero_IATF']}, DG: {i['DG']}, Perda: {i['perda']}"
                for i in inseminacoes
            ])
        ])

        return dados_formatados

    except Exception as e:
        print("❌ ERRO AO BUSCAR DADOS DO BANCO:", str(e))
        return "Não foi possível acessar os dados do banco."

    finally:
        cursor.close()
        conn.close()


# ---------------------------
# ✅ Função para obter histórico do chat do usuário
# ---------------------------
def obter_historico(chat_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT conteudo, origem FROM mensagem 
            WHERE idchat = %s AND idusuario = %s
            ORDER BY enviado_em ASC
        """, (chat_id, usuario_id))
        mensagens = cursor.fetchall()

        # Formatar o histórico para o prompt da LLM
        historico_formatado = "\n".join([
            f"{'Usuário' if msg['origem'] == 'usuario' else 'LLM'}: {msg['conteudo']}"
            for msg in mensagens
        ])

        return historico_formatado

    except Exception as e:
        print("❌ ERRO AO BUSCAR HISTÓRICO:", str(e))
        return ""

    finally:
        cursor.close()
        conn.close()

# ---------------------------
# ✅ Enviar mensagem e obter resposta da OpenAI
# ---------------------------
@mensagem_bp.route('/mensagens', methods=['POST'])
@jwt_required()
def enviar_mensagem():
    usuario_id = get_jwt_identity()
    data = request.json
    chat_id = data.get('idchat')
    conteudo = data.get('conteudo')

    if not conteudo or not chat_id:
        return jsonify({'message': 'Chat ID e conteúdo são obrigatórios'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Salvar a mensagem do usuário no banco
        cursor.execute("INSERT INTO mensagem (conteudo, origem, enviado_em, idusuario, idchat) VALUES (%s, 'usuario', NOW(), %s, %s)",
                       (conteudo, usuario_id, chat_id))
        conn.commit()

        # 2️⃣ Obter histórico do chat
        historico = obter_historico(chat_id, usuario_id)

        # 3️⃣ Obter informações do banco de TODAS AS TABELAS
        dados_banco = obter_dados_do_banco()

        # 4️⃣ Enviar a mensagem para a OpenAI
        resposta_llm = obter_resposta_da_llm(conteudo, historico, dados_banco)

        # 5️⃣ Salvar a resposta da OpenAI no banco
        cursor.execute("INSERT INTO mensagem (conteudo, origem, enviado_em, idusuario, idchat) VALUES (%s, 'LLM', NOW(), %s, %s)",
                       (resposta_llm, usuario_id, chat_id))
        conn.commit()

        return jsonify({'message': 'Mensagem enviada!', 'resposta': resposta_llm}), 201

    except Exception as e:
        conn.rollback()
        print("❌ ERRO NO BACKEND:", str(e))
        return jsonify({'message': 'Erro ao processar mensagem', 'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# ---------------------------
# ✅ Função para chamar a API do ChatGPT (OpenAI)
# ---------------------------
def obter_resposta_da_llm(mensagem_usuario, historico, dados_banco):
    try:
        prompt = f"""
        Você é um assistente virtual especializado em protocolos de inseminação de gado.
        Seu objetivo é ajudar os usuários a encontrar informações sobre os protocolos registrados no banco de dados.

        **Dados do banco de dados:**
        {dados_banco}

        **Histórico da conversa:**
        {historico}

        Agora responda à seguinte pergunta do usuário:
        {mensagem_usuario}
        """

        resposta = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": mensagem_usuario}
            ]
        )

        print("Resposta completa da OpenAI:", resposta)

        return resposta.choices[0].message.content

    except Exception as e:
        print("❌ ERRO NA OPENAI:", str(e))
        return f"Erro ao conectar com a LLM (OpenAI): {str(e)}"

# ---------------------------
# ✅ Listar mensagens de um chat específico
# ---------------------------
@mensagem_bp.route('/mensagens/<int:chat_id>', methods=['GET'])
@jwt_required()
def listar_mensagens(chat_id):
    usuario_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT conteudo, origem, enviado_em FROM mensagem WHERE idchat = %s AND idusuario = %s ORDER BY enviado_em ASC",
            (chat_id, usuario_id)
        )
        mensagens = cursor.fetchall()

        return jsonify({'mensagens': mensagens}), 200

    except Exception as e:
        print("❌ ERRO AO RECUPERAR MENSAGENS:", str(e))
        return jsonify({'message': 'Erro ao recuperar mensagens', 'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
