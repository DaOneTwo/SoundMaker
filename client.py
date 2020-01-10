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

    def conversation(self, text_list: List[Tuple]):
        """play a conversation
        #ToDo: not implemented in other areas will require work in (server & tts.py)
        """
        conversation = []
        for tup in text_list:
            conversation.extend(tup)
        self._send_data(f'conversation|{"|".join(conversation)}')

    # def play_sound(self, sound_name: str, wait: float = 0.0, count: int = 1):
    #     for i in range(count):
    #         self._send_data(f'play|{sound_name}')
    #         self.wait(wait)
    #
    # def play_routine(self, routine: List[Tuple], wait: float = 0.0, repeat: int = 1):
    #     """play a "routine" or a sound arrangement"""
    #     for i in range(repeat):
    #         for item in routine:
    #             self.play_sound(*item)
    #         self.wait(wait)


if __name__ == '__main__':
    sc = TextToSpeechClient(name='Andy', server_ip='127.0.0.1')

    sc.say('Samantha', 'Knock Knock')
    sc.say('Karen', 'Who is there?')
    sc.say('Samantha', 'Etch')
    sc.say('Karen', 'Etch Who')
    sc.say('Samantha', 'Bless You!')
