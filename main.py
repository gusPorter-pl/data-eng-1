from classes import Song, Duration, Time, SongDataFrame
from functions import validate_data, check_error, print_songs

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3

DATABASE = "sqlite:///played_songs.sqlite"
USER_ID = "angusporter7"
O_AUTH_TOKEN = "BQDmm8SvsdRGmvbErVln6u8S4DkxWXLot30Fvg1l2QVK80V0hTp1NiMaPB_z8a8lxDW879zTNZ_gviGJwIu1IQS5FHJS-U4UcRsJTv5FpXkggUDIMdDZgAbt_uZeBj5r8s7jycOEKolCCYVuAHm6uuo9J2V-Uj30pGFxH7OR"
ENDPOINT = "https://api.spotify.com/v1/me/player/recently-played"

def get_timestamp_query():
    today = datetime.datetime.now()  # timestamp right now
    difference = today - datetime.timedelta(days=1)  # difference in datetime objects
    difference_timestamp = int(difference.timestamp()) * 1000  # timestamp difference
    return difference_timestamp

def assess_data(items):
    song_list = []
    for item in items:
        title = item["track"]["name"]
        album = item["track"]["album"]["name"]
        artist = item["track"]["artists"][0]["name"]
        duration = Duration(item["track"]["duration_ms"])
        time_played = Time(item["played_at"])
        song_list.append(Song(title, album, artist, duration, time_played))
    return song_list

def main():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {O_AUTH_TOKEN}"
    }
    difference_timestamp = get_timestamp_query()
    req = requests.get(f"{ENDPOINT}?after={difference_timestamp}", headers=headers)
    data = req.json()
    check_error(data)
    songs = assess_data(data["items"])
    song_dataframe = SongDataFrame(songs)
    if validate_data(song_dataframe.data):
        print_songs(songs)
        print(song_dataframe.data)

if __name__ == "__main__":
    main()
