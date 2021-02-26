import librosa, soundfile
from pydub import AudioSegment

y, sr = librosa.load("./bruh.mp3")

y_pitched = librosa.effects.pitch_shift(y, sr, n_steps=4)

soundfile.write("bruv.ogg", y_pitched, sr)

sound = AudioSegment.from_wav("./bruv.wav")
sound.export("bruv.mp3", format="mp3")
