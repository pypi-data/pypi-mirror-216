import asyncio
import websockets
import ssl
import uuid
import certifi
import requests

class Receiver:
    def _generate_unique_id():
        return str(uuid.uuid4())

    def __init__(self, process_message, client_id, API_KEY):
        self.websocket = None
        self.client_id = client_id if client_id else Receiver._generate_unique_id()
        self.received_message = None
        self.process_message = process_message
        self.API_KEY = API_KEY

    async def receive_message(self):
        while True:
            received_message = await self.websocket.recv()
            response = self.process_message(received_message)
            await self.websocket.send(response)

    async def _connect_to_server(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        remote_url = 'wss://vocalhost.reiserx.com/'

        try:
            async with websockets.connect(remote_url+'ws/?client_id=' + self.client_id + '&api_key='+self.API_KEY, ssl=ssl_context) as websocket:
                print("Connected: " + self.client_id)
                self.websocket = websocket
                await self.receive_message()

        except websockets.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
            # Handle connection closure, if needed

        except Exception as e:
            print(f"Error occurred: {e}")
            
    def connect(self):
        asyncio.run(self._connect_to_server())


class Request:
    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, message, receiver_id, timeout=60):
        receiver_id = str(receiver_id)
        self.url = 'https://vocalhost.reiserx.com/connect/'+ receiver_id +'/'
        data = {
            'message': message
        }
        
        self.headers = {
            'Timeout': str(timeout),
            'Authorization': self.api_key
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        return response
