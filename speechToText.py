import numpy as np
import whisper
import torchaudio

class SpeechToText:

    def __init__(self, model: str="base"):
        # possible models: "tiny", "base", "small", "medium", "large"
        self.model = whisper.load_model(model)

    def transcribeFile(self, filepath: str="output.wav"):
        result = self.model.transcribe(filepath)
        return result["text"]