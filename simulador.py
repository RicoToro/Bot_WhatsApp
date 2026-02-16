import requests
import time

URL = "http://127.0.0.1:5000/webhook"

def simular_envio():
    while true:
        print("\n" + "="*30)
        msg = input("Digite sua mensagem (ou 'sair'):")
        if msg.lower() == 'sair' : break

        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "5511999999999",
                            "text": {"body": msg}
                        }]
                    }
                }]
            }]
        }
        try:
            requests.post(URL, json=payload)
            print("Mensagem enviada ao servidor!")
        except:
            print("Erro: o app .py está rodando?")
    simular_envio()
