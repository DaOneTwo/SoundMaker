import socket
from time import sleep
from typing import List, Tuple


class SocketClient:
    def __init__(self, name, server_ip='127.0.0.1', server_port=30000):
        self.client_name = name
        self.server_address = (server_ip, server_port)

        self.register_client()

    def _send_data(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        sock.sendto(data.encode(), self.server_address)
        sock.close()

    def register_client(self):
        self._send_data(f'register|{self.client_name}')

    def wait(self, seconds: float):
        sleep(seconds)


class TextToSpeechClient(SocketClient):
    def __init__(self, name, server_ip='127.0.0.1', server_port=30000):
        super().__init__(name=name, server_ip=server_ip, server_port=server_port)

    def say(self, voice: str, text: str):
        self._send_data(f'say|{voice}|{text}')


if __name__ == '__main__':
    sc = TextToSpeechClient(name='Your Name Here', server_ip='127.0.0.1')
    
    sc.say('Samantha', 'Knock Knock')
    sc.wait(1.2)
    sc.say('Karen', 'Who is there?')
    sc.wait(1.3)
    sc.say('Samantha', 'Etch')
    sc.wait(.75)
    sc.say('Karen', 'Etch Who')
    sc.wait(.90)
    sc.say('Samantha', 'Bless You!')

