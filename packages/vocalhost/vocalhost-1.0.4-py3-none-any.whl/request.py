import requests

class VocalhostClient:
    def __init__(self, api_key, receiver_id=None):
        self.api_key = api_key
        self.receiver_id = receiver_id
        self.url = 'https://vocalhost.reiserx.com/'+ receiver_id +'/'
        self.headers = {
            'Timeout': '100',
            'Authorization': self.api_key
        }

    def send(self, message):
        data = {
            'message': message
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        return response
