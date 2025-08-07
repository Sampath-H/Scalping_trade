import requests

TOKEN = "8356703064:AAEMhsjLDQA8XKp80Gh-IwYMCoGKBQdOOTc"
CHAT_ID = "1042202004"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)