from os import listdir, remove
from os.path import isdir
import librosa, soundfile
from pydub import AudioSegment
import threading


def loadFiles(path):
    dirList = listdir(path)
    songList = []

    for dir in dirList:
        if isdir(path + "\\" + dir):
            temp = listdir(path + "\\" + dir)
            for file in temp:
                if file.endswith(".mp3"):
                    songList.append(path + "\\" + dir + "\\" + file)
    return songList


def pitchSong(path, steps):
    y, sr = librosa.load(path)
    y_pitched = librosa.effects.pitch_shift(y, sr, n_steps=steps)

    remove(path)

    path = path.replace(".mp3", "")

    soundfile.write(path + ".wav", y_pitched, sr)

    sound = AudioSegment.from_wav(path + ".wav")
    sound.export(path + ".mp3", format="mp3")


def main():
    path = input("Please input Song Folder Path")
    steps = input("By how much do you want to pitch the songs (-10, 10)")
    songList = loadFiles(path)

    for song in songList:
        print(threading.active_count())
        if threading.active_count() <= 2:
            threading.Thread(target=pitchSong, args=(song, steps)).start()
            continue
        print("here")
        pitchSong(song, steps)


main()
