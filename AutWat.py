from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
ACCESS_TOKEN = "EAAXGbKZCTZCnUBQvMkkVjpTA8YPnt0bD3e6v4HOOcXI3ERfrGe8vmd5smYzegr19Cdc1R8GMSl9IEu9A0q2GkBfNXezIo1M1ZAu8THYZAUvAFJXjOyWYZCUuFihkOx4BjjOx6qbT26XupfROcrTkjD2rsDlyokHRFyHkS84iHS25cZBfLFXopeNiwqOybt0cJ4ESv0H2iEwtXQhrhv0CtfzIP1F3YKyR4fKi5M3ES1Yw6Ljirtt3kszfk56KTCwkoY8thbZBfz5rphKuNyuJMkzPweVweEq31y1C6BPaAZDZD"
PHONE_NUMBER_ID = "1049805381541277"
VERIFY_TOKEN = "Pedro1301" 
VERSION = "v18.0"

# --- Carregamento de Dados ---
def carregar_respostas():
    """Lê o arquivo JSON. Se der erro, cria um padrão."""
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'respostas.json')
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("ERRO: Arquivo respostas.json não encontrado!")
        return {"padrao": "Erro interno: Base de dados não encontrada."}

# --- Lógica Do Bot ---
def processar_texto(texto_recebido):
    """Analisa o texto e busca a resposta no JSON"""
    texto = texto_recebido.lower().strip()
    dados = carregar_respostas() # Carrega a cada mensagem (atualização em tempo real)
    
    # Busca por palavras-chave
    for chave, resposta in dados.items():
        if chave in texto and chave != "padrao":
            return resposta
            
    # Caso não encontrar nada
    return dados.get("padrao", "Desculpe, não entendi.")

# --- Envio WhatsApp ---
def enviar_resposta_whatsapp(numero, texto):
    """Envia a resposta de volta para a API da Meta"""
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    
    try:
        # Só tenta enviar se tivermos um token configurado
        if ACCESS_TOKEN != "SEU_TOKEN_PERMANENTE_AQUI":
            response = requests.post(url, headers=headers, json=data)
            print(f"Status envio WhatsApp: {response.status_code}")

            print(f"RESPOSTA DO FACEBOOK: {response.json()}")
        else:
            print(f"MODO SIMULAÇÃO: Mensagem não enviada para a API (Token ausente).")
            print(f"Para o número {numero}: {texto}")
            
    except Exception as e:
        print(f"Erro ao enviar: {e}")

# --- Rotas ---
@app.route('/webhook', methods=['GET'])
def verify():
    """Verificação inicial do Facebook"""
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Falha na verificação", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe mensagens"""
    data = request.get_json()
    
    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' in value:
            message = value['messages'][0]
            numero = message['from']
            texto_usuario = message['text']['body']
            
            print(f"\n📩 Recebido de {numero}: {texto_usuario}")
            
            # 1. Pensa
            resposta_bot = processar_texto(texto_usuario)
            
            # 2. Responde
            enviar_resposta_whatsapp(numero, resposta_bot)
            
    except Exception as e:
        pass

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    print("Servidor rodando! Aguardando mensagens...")
    app.run(port=5000, debug=True)