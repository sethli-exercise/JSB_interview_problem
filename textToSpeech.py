import pyttsx3

class TextToSpeech:

    def __init__(self, volume: float=0.5):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', volume)

    def setVolume(self, volume: float):
        self.engine.setProperty('volume', volume)

    def speakText(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError as e:
            # engine is already talking do nothing
            return

    def stop(self):
        self.engine.stop()