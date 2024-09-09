# from twilio.rest import Client
import random

import vonage

from dotenv import load_dotenv
import os

load_dotenv()


def generate_otp():
    code = str(random.randint(100000, 999999))
    return f"{code[:3]}-{code[3:]}"


# def send_otp(number, otp):
#     account_sid = "your_twilio_account_id"
#     auth_token = "your_twilio_auth_token"

#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body=f"Votre code de vérification est {otp}",
#         from_="+123456789",  # Numero Twilio
#         to=number,
#     )
#     return message.sid


def send_otp_vonage(number, otp):
    client = vonage.Client(key=os.environ.get('VONAGE_API_KEY') , secret=os.environ.get('VONAGE_API_SECRET'))
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Jobers Artisans",
            "to": str(number),
            "text": f"Votre code de vérification est {otp}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        return("Message envoyé avec succès")
    else:
        return(f"Message failed with error: {responseData['messages'][0]['error-text']}")


import requests
import json



# Envoi de l'otp par whatsapp

url = "https://graph.facebook.com/v20.0/406813785846103/messages"

def send_otp_whatsapp(number:str, otp:str):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": "envoi_otp",
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": otp
                            }
                        ]
                    }
                ],
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.environ.get('WHATSAPP_TOKEN'), # installer dotenv pour gerer la confidentialite des cles...
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return ("Message envoyé avec succès")
    else:
        return(f"Message non envoyé : {response.text}")

# send_otp_whatsapp("+22891657590", "596-895")