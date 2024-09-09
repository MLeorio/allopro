from dotenv import load_dotenv
import os

import random

import requests
import json

load_dotenv()


def generate_otp():
    return str(random.randint(100000, 999999))


# Envoi de l'otp par whatsapp

def send_otp_whatsapp(number: str, otp: str):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": "envoi_otp",
                "language": {"code": "fr"},
                "components": [
                    {"type": "body", "parameters": [{"type": "text", "text": otp}]}
                ],
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.environ.get(
            "WHATSAPP_TOKEN"
        ),  # installer dotenv pour gerer la confidentialite des cles...
    }

    response = requests.request(
        "POST",
        os.environ.get("WHATSAPP_API_URL"),
        headers=headers,
        data=payload
    )

    if response.status_code == 200:
        return "Message envoyé avec succès"
    else:
        return f"Message non envoyé : {response.text}"


# send_otp_whatsapp("+22891657590", "596-895")


# Envoie de sms par Unimatrix

from uni.client import UniClient
from uni.exception import UniException



# def send_otp_unimatrix(number: str, otp: str): # methode utilisant le SDK
#    client = UniClient(os.environ.get("UNIMTX_ACCESS_KEY_ID"))
#     try:
#         res = client.messages.send(
#             {
#                 "to": number,
#                 "signature": "AlloProo",
#                 "templateId": "pub_otp_fr",
#                 "templateData": {"code": otp},
#             }
#         )
#         print(res.data)
#     except UniException as e:
#         print(e)



def send_otp_unimax(number: str, otp: str): # methode utilisant le lien d'API
    payload = json.dumps(
        {
            "to": number,
            "text": f"[AlloProo] Votre code de vérification est {otp}."
        }
    )
    headers = {
        "Content-Type": "application/json",
        }
    
    url = f'https://api.unimtx.com/?action=sms.message.send&accessKeyId={os.environ.get("UNIMTX_ACCESS_KEY_ID")}'

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload
    )

    if response.status_code == 200:
        return "Message envoyé avec succès"
    else:
        return f"Message non envoyé : {response.text}"


# send_otp_unimax("+22891657590", "596895")