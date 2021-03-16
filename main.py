from classes import Song, Duration, Time, SongDataFrame
from functions import validate_data, check_error, print_songs

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3

TABLE = "played_songs"
FILE = f"{TABLE}.sqlite"
DATABASE = f"sqlite:///{FILE}"
USER_ID = "angusporter7"
O_AUTH_TOKEN = "BQC7PPR8PAd8QfzZUGLKY5sEezwiS-ZpD03jAlc8XjyjZpDfxa5AbsN2L7KkwG6QSpKm2v8f8G2_Kd68V502FhD5nIbstGNC9fgugMiF0xKeFYOXvGgCTENnFVQ7gFHJsT5ZtrMX_gWHYZEo-2A8tpqLJ_To-D9RefNt-DjV"
ENDPOINT = "https://api.spotify.com/v1/me/player/recently-played"

def get_timestamp_query():
    today = datetime.datetime.now()  # timestamp right now
    difference = today - datetime.timedelta(days=1)  # difference in datetime objects
    difference_timestamp = int(difference.timestamp()) * 1000  # timestamp difference
    return difference_timestamp

def create_song_list(items):
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
    # EXTRACT
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {O_AUTH_TOKEN}"
    }
    difference_timestamp = get_timestamp_query()
    req = requests.get(f"{ENDPOINT}?after={difference_timestamp}", headers=headers)
    data = req.json()
    check_error(data)
    songs = create_song_list(data["items"])
    song_dataframe = SongDataFrame(songs)

    # VALIDATE
    if validate_data(song_dataframe.data):
        print_songs(songs)
        print(song_dataframe.data)

    # LOAD
    engine = sqlalchemy.create_engine(DATABASE)
    conn = sqlite3.connect(FILE)
    cursor = conn.cursor()
    query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
            title VARCHAR(128),
            album VARCHAR(128),
            artist VARCHAR(128),
            duration VARCHAR(128),
            time_played VARCHAR(128),
            PRIMARY KEY (time_played)
        );
    """
    cursor.execute(query)
    print("Executed create table query")
    
    try:
        song_dataframe.data.to_sql(TABLE, engine, index=False, if_exists="append")
    except:
        print("Data already exists in the database")
    finally:
        print("Executed update table query")
        conn.close()

if __name__ == "__main__":
    main()
