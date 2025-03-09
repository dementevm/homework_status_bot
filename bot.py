import requests


class TelegramBot:
    def __init__(self, token:str):
        self.url = 'https://api.telegram.org/'
        self.token = f'bot{token}/'

    def send_message(self, text: str, chat_id: int | str) -> None:
        method = 'sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        endpoint = self.url + self.token + method
        r = requests.post(url=endpoint, json=payload)
        if r.status_code != 200:
            payload = {
                'chat_id': chat_id,
                'text': {'status_code': r.status_code, 'error': r.json()}
            }
            requests.post(url=endpoint, json=payload)

