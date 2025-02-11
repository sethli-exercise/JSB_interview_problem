import pocketsphinx
from pocketsphinx import LiveSpeech, get_model_path


class SpeechToText:
    def __init__(self):
        model_path = get_model_path()

        self.config = pocketsphinx.Decoder.default_config()
        self.config.set_string('-hmm', model_path + '/en-us')
        self.config.set_string('-lm', model_path + '/en-us.lm.bin')
        self.config.set_string('-dict', model_path + '/cmudict-en-us.dict')
        self.decoder = pocketsphinx.Decoder(self.config)

    def transcribe_from_wav(self, audio_file):
        with open(audio_file, "rb") as f:
            audio_data = f.read()

        self.decoder.start_utt()
        self.decoder.process_raw(audio_data, False, True)
        self.decoder.end_utt()

        return self.decoder.hyp().hypstr if self.decoder.hyp() else ""

    def transcribe_live(self):
        print("Listening... Speak now.")
        speech = LiveSpeech()
        for phrase in speech:
            print("You said:", phrase)