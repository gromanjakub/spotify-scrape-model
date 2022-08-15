import spotipy.util as util
import pandas as pd
import requests
import logging
import json


logger = logging.getLogger(__file__)
#logging, try/except, duplicita kodu, type hints (sipky atd), unit test

def foo(config_path: str):
    try:
        with open(config_path, 'r') as f:
            config = f.read()
    except FileNotFoundError as e:
        logger.error("smrtjrtjrj")
        raise e

def generate_token(config_path: str) -> str:
    """generate token to access Spotify API

    Args:
        config_path: Path to config file containing secrets, e.g. /home/jgroman/repo/config.json

    Returns:
        str: token
    """
    # How to import variables from json file
    # How to get credentials to spotify - put in readme, remove comments in this fun
    dictionary = {}
    config= open("spotify_config.json")
    config_data = json.load(config)
    username = config_data["username"]
    client_id = config_data["client_id"]
    client_secret = config_data['client_secret'] #produced on Spotify Developers site
    config.close()
    redirect_uri = 'http://localhost:7777/callback' #the spotify api requires a redirect URI
    scope = 'user-library-read'
    token = util.prompt_for_user_token(
        username=username, 
        scope=scope, 
        client_id=client_id,   
        client_secret=client_secret,     
        redirect_uri=redirect_uri
    )
    return token # add


def get_headers(token: str) -> dict:
    """get headers used in API requests

    Args:
        token (str): _description_

    Returns:
        dict: headers
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + token,
    }
    return headers


def get_songs(limit: int, headers: dict, offset: int):
    """fetches a list of songs

    Args:
        limit (int): _description_
        headers (dict): _description_
        offset (int): _description_

    Returns:
        list: song_list
    """
    loaded_songs = requests.get(f'https://api.spotify.com/v1/me/tracks?limit={limit}&offset=' + str(offset), headers=headers)
    song_list = []
    for song in range(len(loaded_songs.json()["items"])):
        song_list.append(loaded_songs.json()["items"][song]["track"]["id"])
    return song_list


def get_ids(token: str) -> pd.DataFrame:
    """get ids of songs used for the model, store in df

    Args:
        token (str): token generated by generate_token()

    Returns:
        pd.DataFrame: pd.df of songs and their ids
    """
    headers = get_headers(token)
    spotify_songs = []
    offset = 0
    while offset < 7: #spotify API allows downloading only up to 50 songs at a time, offset parameter allows to access more
        song_list = get_songs(50, headers, offset)
        spotify_songs.append(song_list)
        offset = offset +1
    if offset == 7:
        song_list = get_songs(7, headers, offset)
        spotify_songs.append(song_list)
    
    flat_spotify_songs  = sum((spotify_songs), [])

    offset2 = 0
    not_liked_list = [] #in order to produce a model, I created (and downloaded here) a playlist of songs I do not have in my liked songs
    while offset2 < 17:
        # add api parameter to get_songs to include not_liked_songs
        not_liked_playlist = requests.get('https://api.spotify.com/v1/playlists/0l6KZUCPhG7ypHHBGhXb5s/tracks?limit=50', headers=headers)
        not_liked_playlist.json()
        for song in range(len(not_liked_playlist.json()["items"])):
            not_liked_list.append(not_liked_playlist.json()["items"][song]["track"]["id"])   
        offset2 = offset2+1

    # separate into its own function
    df_liked = pd.DataFrame(flat_spotify_songs, columns = ["id"])
    df_liked["liked"] = 1 #songs in my library
    df_not_liked = pd.DataFrame(not_liked_list, columns = ["id"])
    df_not_liked["liked"] = 0 
    df = pd.concat([df_liked, df_not_liked])
    df = df.sample(frac=1).reset_index(drop=True)
    return(df)

def get_features(token: str, df: pd.DataFrame) -> pd.DataFrame:
    """adds parameters to song ids

    Args:
        token (str): _description_
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: df with ids and all parameters
    """
    headers = get_headers(token)

    for index, row in df.iterrows():
        try: #some songs (47) return a KeyError, this is is the fastest way to get rid of them
            row_features = requests.get('https://api.spotify.com/v1/audio-features/'+row["id"], headers=headers)
            df.loc[index, "danceability"] = row_features.json()["danceability"]
            df.loc[index, "energy"] = row_features.json()["energy"]
            df.loc[index, "key"] = row_features.json()["key"]
            df.loc[index, "loudness"] = row_features.json()["loudness"]
            df.loc[index, "mode"] = row_features.json()["mode"]
            df.loc[index, "speechiness"] = row_features.json()["speechiness"]
            df.loc[index, "acousticness"] = row_features.json()["acousticness"]
            df.loc[index, "instrumentalness"] = row_features.json()["instrumentalness"]
            df.loc[index, "liveness"] = row_features.json()["liveness"]
            df.loc[index, "valence"] = row_features.json()["valence"]
            df.loc[index, "tempo"] = row_features.json()["tempo"]
            df.loc[index, "duration_ms"] = row_features.json()["duration_ms"]
            df.loc[index, "time_signature"] = row_features.json()["time_signature"]
        except KeyError: 
            pass
    df.dropna(inplace = True) #this gets rid of the songs producing a KeyError (all NA)
