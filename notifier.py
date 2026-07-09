import requests
import urllib.parse


class WhatsAppNotifier:
    def __init__(self, phone, apikey):
        self.phone = phone
        self.apikey = apikey

    def send_alert(self, message):
        text = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={self.phone}&text={text}&apikey={self.apikey}"
        try:
            response = requests.get(url, timeout=10)
            print(f"WhatsApp alert sent: {response.status_code}")
        except Exception as e:
            print(f"Failed to send WhatsApp alert: {e}")