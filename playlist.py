import os
import random

from pygame import mixer


class PlayList:
    def __init__(self) -> None:
        self._track_files = []
        self._track_number = 0
        mixer.init()
        mixer.music.set_volume(0.7)

    def load(self, folder_name: str) -> None:
        for _, _, files in os.walk(folder_name):
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension in [".mp3", ".ogg"]:
                    self._track_files.append(os.path.join(folder_name, file))
        self._remove_invalid_tracks()

    def _remove_invalid_tracks(self):
        for track in self._track_files:
            try:
                mixer.load(track)
            except:
                self._track_files.remove(track)

    def play_track(self, i: int) -> None:
        if len(self._track_files)>0:
            mixer.music.load(self._track_files[i])
            mixer.music.play()

    def check(self) -> None:
        if mixer.music.get_busy():
            return
        self._track_number += 1
        if self._track_number >= len(self._track_files):
            random.shuffle(self._track_files)
            self._track_number = 0
        self.play_track(self._track_number)

    def start(self) -> None:
        random.shuffle(self._track_files)
        self._track_number = 0
        self.play_track(0)

    def stop(self) -> None:
        mixer.music.stop()
