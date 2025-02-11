import pyaudio
import wave

class AudioRecorder:
    def __init__(self, filename="output.wav", duration=5, rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
        self.filename = filename
        self.duration = duration
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.audio = pyaudio.PyAudio()

    def record(self):
        print("Recording...")
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)

        frames = []
        for _ in range(0, int(self.rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        self._save_audio(frames)

    def _save_audio(self, frames):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved as {self.filename}")