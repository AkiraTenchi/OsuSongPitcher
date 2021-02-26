import os
from os.path import isdir
import librosa, soundfile
from pydub import AudioSegment


def loadFiles(path):
    dirList = os.listdir(path)
    songList = []

    for dir in dirList:
        if isdir(path + "\\" + dir):
            temp = os.listdir(path + "\\" + dir)
            for file in temp:
                if file.endswith(".mp3"):
                    songList.append(path + "\\" + dir + "\\" + file)
    return songList


def pitchSong(path):
    y, sr = librosa.load(path)
    y_pitched = librosa.effects.pitch_shift(y, sr, n_steps=4)

    os.remove(path)

    path = path.replace(".mp3", "")

    soundfile.write(path + ".wav", y_pitched, sr)

    sound = AudioSegment.from_wav(path + ".wav")
    sound.export(path + ".mp3", format="mp3")


def main():
    path = input("Please input Song Folder Path")
    songList = loadFiles(path)
    print(songList)
    for song in songList:
        pitchSong(song)


main()