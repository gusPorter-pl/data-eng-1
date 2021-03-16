import datetime
import pandas as pd

"""
Checks to see if the data sent through is valid
Params: Takes panda dataframe
Return: Boolean that shows if data is integral
"""
def validate_data(data: pd.DataFrame) -> bool:
    if data.empty:
        print("No songs listened to today")
        return False
    if not pd.Series(data["time_played"]).is_unique:
        raise Exception("Data does not contain primary keys")
    if data.isnull().values.any():
        raise Exception("None value in data")
    
    difference = datetime.datetime.now() - datetime.timedelta(days=1)

    timestamps = data["time_played"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") < difference:
            raise Exception("Time played does not occur in the past 24 hours")

    return True

"""
Checks if an error message has been passed
"""
def check_error(data):
    if "error" in data:
        raise Exception(f"\n{data['error']['status']}: {data['error']['message']}")

"""
Prints songs through a for loop
"""
def print_songs(songs):
    # print(json.dumps(items[0], indent=4, sort_keys=True))
    for song in songs:
        print(f"{song}\n")