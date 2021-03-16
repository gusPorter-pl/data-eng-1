import pandas as pd

class Duration:
    def __init__(self, duration: int):
        self.__duration = duration  # milliseconds
    
    def __str__(self):
        second_length = self.__duration // 1000
        if second_length % 60 < 10:
            return f"{second_length // 60}:0{second_length % 60}"
        else:
            return f"{second_length // 60}:{second_length % 60}"

class Time:
    def __init__(self, time: str):
        self.time = time
    
    def __str__(self):
        return f"{self.time[0: 10]} {self.time[11: 23]}"

class Song:
    def __init__(self, title: str, album: str, artist: str, duration: Duration, time_played: Time):
        self.title = title
        self.album = album
        self.artist = artist
        self.duration = duration
        self.time_played = time_played

    def __str__(self):
        return f"Title: {self.title}\nAlbum: {self.album}\nArtist: {self.artist}\nDuration: {self.duration}\nTime Played: {self.time_played}"

class SongDataFrame:
    def __init__(self, songs):
        self.songs = songs
        self.data = self.__create_dataframe()
    
    def __create_dataframe(self):
        song_dict = {
            "title": [song.title for song in self.songs],
            "album": [song.album for song in self.songs],
            "artist": [song.artist for song in self.songs],
            "duration": [song.duration.__str__() for song in self.songs],
            "time_played": [song.time_played.__str__() for song in self.songs]
        }
        return pd.DataFrame(song_dict, columns=("title", "album", "artist", "duration", "time_played"))