from pathlib import Path
import socket
import threading
import subprocess
from queue import Queue

import playsound
import pyttsx3

from logger import get_logger


class SocketServer:
    """a very basic socket server establishes a listening socket.  Inbound requests are simply put in
    a queue.  Nothing else is done with them.  Mixin classes inheriting/extending objects will need to add their
    own message processing capabilities.
    """

    def __init__(self, listen_port: int = 30000, log_level='DEBUG'):
        self.logger = get_logger(level=log_level)
        self.running = True

        self._listen_socket = None
        self._listen_port = listen_port
        self._listen_thread = None
        self.inbound_msg_queue = Queue()

    def _start_listen_thread(self):
        """start a socket listener and related thread"""
        self._listen_socket = socket.socket(type=socket.SOCK_STREAM)
        self._listen_socket.bind(('', self._listen_port))
        self._listen_socket.listen(5)
        self.logger.info(f'listen socket created. {self._listen_socket}')

        self._listen_thread = threading.Thread(name='listen_thread', target=self._receive_messages)
        self._listen_thread.start()
        self.logger.info(f'listen thread is running: {self._listen_thread.is_alive()}')

    def _receive_messages(self):
        """This method accepts connections, receives messages and add them to the inbound_queue.
        This is run in a thread. started in _start_listen_thread"""
        while self.running is True:
            connection, client_address = self._listen_socket.accept()
            try:
                self.logger.debug(f'connection received from {client_address}')
                data = ''
                while True:
                    part = connection.recv(1024)
                    if not part:
                        break
                    data += part.decode()
                connection.close()
                self.logger.debug(f'data received: {data}')
                self.inbound_msg_queue.put_nowait(item=(client_address, data))
            except:
                pass

    def run(self):
        """Start up the server.  Starts listening thread"""
        self._start_listen_thread()


class TextToSpeechServer(SocketServer):
    base_fp = Path(__file__).parent
    sounds_fp = Path(base_fp.joinpath('sounds'))

    def __init__(self, listen_port: int = 30000, log_level='DEBUG', welcome_new_clients: bool = False,
                 use_action_thread: bool = True):
        super().__init__(listen_port=listen_port, log_level=log_level)
        self.welcome_new_clients = welcome_new_clients
        self.use_action_thread = True

        self._processing_thread = None
        self.action_q = Queue()

        self.clients = {}
        self.voices = self._get_voices()

        self.func_map = {
            'register': self._register_client,
            'say': self._text_to_speech
            # 'conversation':
        }

    def _start_processing_thread(self):
        self._processing_thread = threading.Thread(name='processing_thread', target=self._handle_requests)
        self._processing_thread.start()

    def _handle_requests(self):
        while self.running is True:
            request = self.inbound_msg_queue.get()
            self._handle_request(request)

    def _handle_request(self, request: tuple):
        """a request is stored in the form of a tuple... (('127.0.0.1', 56868), 'register|YourName')"""
        connection_details, data = request
        ip, port = connection_details
        command, *data = data.split('|')
        # get the function for the command passed and execute it.
        command_func = self.func_map.get(command)
        if self.use_action_thread is True:
            exec_thread = threading.Thread(target=command_func, args=(ip, data), daemon=True)
            exec_thread.start()
        else:
            command_func(ip, data)

    def _register_client(self, ip, data):
        name = data[0]
        if all([ip, ip not in self.clients]):  # allows me to run things internally and not register and trigger welcome
            # implement welcome message easter egg for newly registered clients
            if self.welcome_new_clients is True:
                self._welcome_new_client(name)
            self.clients[ip] = name
            self.logger.info(f'registered client {name} with the ip {ip}')

    def _welcome_new_client(self, name: str):
        """plays a welcome for newly registered IPs only when configuration self.welcome_new_clients is True"""

        playsound.playsound(str(self.sounds_fp.joinpath('Doorbell.wav')), block=True)
        welcome_message = f'Hey everyone! {name} made it!  What a smarty pants!'
        self._text_to_speech(ip='', data=['Samantha', welcome_message])
        playsound.playsound(str(self.sounds_fp.joinpath('applause5.mp3')), block=True)

    # def _text_to_speech(self, ip, data):
    #     client_name = self._get_client_name(ip)
    #     voice, text = data
    #     self.chatter_bot.setProperty('voice', self.voices.get(voice.lower()))
    #     self.chatter_bot.say(text)
    #     self.chatter_bot.runAndWait()

    def _text_to_speech(self, ip, data):
        try:
            client_name = self._get_client_name(ip)
            voice_name, text = data
            name = self.voices.get(voice_name.lower(), '')
            # DO NOT like this subprocess thing but use it because of some issues with the open source modules and
            # threads on OSX operating systems.  This slows things down incredibly and lessens the experience a little.
            file_path = str(self.base_fp.joinpath("tts.py"))
            self.logger.debug(f'submitting subprocess for: {voice_name}, {text}')
            x = subprocess.run(["python3", file_path, name, text], stdout=subprocess.PIPE)
            self.logger.debug(f'subprocess result: {x.returncode}')
        except Exception as err:
            self.logger.error(str(err))

    def _get_client_name(self, ip) -> str:
        """get the name registered for this client IP"""
        return self.clients.get(ip, ip)

    def _get_voices(self) -> dict:
        """get the voices available for this server in a dictionary format.
        key: voice name lowered
        value: the id that needs to be used to set the voice
        """
        chatter_bot = pyttsx3.init()
        return {voice.name.lower(): voice.id for voice in chatter_bot.getProperty('voices')}


    def run(self):
        """Start the server.   starts listening thread then starts our message processing thread."""
        super().run()
        self._start_processing_thread()

        self._text_to_speech(ip='', data=('Samantha', 'Server is Ready'))


# class SoundServer:
#     this_dir = Path(__file__).parent
#     # media_dir = str(this_dir.joinpath('media'))
#     _server = None
#     _clients = {}
#
#     def __init__(self, listen_port=None):
#         # self.sound_dict = {}
#         # self.sounds = self.load_sounds()
#
#         self._listen_port = listen_port or 30000
#
#         self._chatter_bot = pyttsx3.init()
#         self._voices = {voice.name.lower(): voice.id for voice in self._chatter_bot.getProperty('voices')}
#
#         # self._start_socket_listener()
#         #
#         # self._start_pyglet_app()
#
#     # def load_sounds(self, path=None):
#     #     """loads all wav sounds in the provided dir"""
#     #     dir = path or self.media_dir
#     #     fp = Path(dir)
#     #     if not fp.is_dir():
#     #         raise FileNotFoundError(f'path provided is not a directory. {dir}')
#     #
#     #     for f in fp.glob('*.wav'):
#     #          self.sound_dict[Path(f).stem] = pyglet.media.load(f, streaming=False)
#
#     def _start_socket_listener(self):
#         """start a socket listener"""
#         self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self._server.settimeout(.001)
#         self._server.bind(('', self._listen_port))
#         print(f'listening on port {self._listen_port}')
#
#     def _get_socket_data(self, *args, **kwargs):
#         """get data off our socket"""
#         try:
#             packet, client = self._server.recvfrom(8192)
#             self.handle_packet(packet, client)
#         except Exception as err:
#             pass
#
#     def handle_packet(self, packet, client):
#         print(f'{self._clients.get(client[0], client[0])} says {packet}')
#         packet = packet.decode()
#         command, *data = packet.split('|')
#         if command == 'register':
#             # enters or updates IP to client name map
#             self._clients[client[0]] = data[0].strip()
#         # elif command == 'play':
#         #     self.sound_dict[data[0].strip()].play()
#         elif command == 'talk':
#             self._say_text(*data)
#         print('packet processed successfully')
#
#     # def _say_text(self, name, text):
#     #     try:
#     #         # DO NOT like this subprocess thing but use it because of some threading issues on OSX operating systems
#     #         # slows things down incredibly.
#     #         subprocess.run(["python3", str(self.this_dir.joinpath("tts.py")), name,  text])
#     #     except:
#     #         pass
#
#     def _say_text(self, name, text):
#         try:
#             self._chatter_bot.setProperty('voice', self._voices.get(name.lower()))
#             self._chatter_bot.say(text)
#             self._chatter_bot.runAndWait()
#         except Exception as err:
#             pass
#
#     # def _start_pyglet_app(self):
#     #     """setup and start our pyglet app.  Will fetch socket data 60 times a second"""
#     #     # pyglet.window.Window(1200, 675)
#     #     pyglet.clock.schedule_interval(self._get_socket_data, 1/60.)
#     #     pyglet.app.run()


if __name__ == '__main__':
    server = TextToSpeechServer(welcome_new_clients=True, use_action_thread=True)
    server.run()

    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(voice.name, voice.id)
    #     engine.setProperty('voice', voice.id)
    #     engine.say('The quick brown fox jumped over the lazy dog.')
    # engine.runAndWait()
