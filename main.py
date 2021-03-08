from os import listdir, remove
from os.path import isdir
import librosa, soundfile
from pydub import AudioSegment
import threading
import multiprocessing

# returns all the paths for the mp3 files as a list
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


def pitchSongs(paths, steps):
    for song in paths:
        pitchSong(song, steps)
    print("done Pitching")


# pitch shift the song by the requested amount
def pitchSong(path, steps):
    print("pitching: " + path)
    y, sr = librosa.load(path)
    y_pitched = librosa.effects.pitch_shift(y, sr, n_steps=steps)

    remove(path)

    path = path.replace(".mp3", "")

    soundfile.write(path + ".wav", y_pitched, sr)

    # convert the wav output to mp3
    sound = AudioSegment.from_wav(path + ".wav")
    sound.export(path + ".mp3", format="mp3")


def main():

    # Necessary input + validation
    path = input("Please input Song Folder Path")
    try:
        steps = int(input("By how much do you want to pitch the songs (-10, 10)"))
        threads = int(input("How many threads do you want to use?"))
    except Exception:
        print("invalid input")
        return

    if (
        not isdir(path)
        or steps > 10
        or steps < -10
        or multiprocessing.cpu_count() - 2 < threads
    ):
        print("invalid input")
        return

    songList = loadFiles(path)
    listChunks = int(len(songList) / threads)

    for i in range(0, threads - 1):
        threading.Thread(
            target=pitchSongs,
            args=(songList[i * listChunks : (i + 1) * listChunks], steps),
        ).start()

    pitchSongs(songList[(threads - 1) * listChunks : len(songList)], steps)


main()
