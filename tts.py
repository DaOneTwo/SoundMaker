import pyttsx3
import sys


class TTS:
    engine = pyttsx3.init()

    def say(self, voice, text):
        """voice is the voice id needed by the application"""
        self.engine.setProperty('voice', voice)
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == '__main__':
    TTS().say(sys.argv[1], sys.argv[2])
    sys.exit()
