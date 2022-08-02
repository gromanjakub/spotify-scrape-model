import spotipy.util as util
import pandas as pd
import requests

def scrape_preload():
    

    username = 'gromja'
    client_id =':)'
    client_secret = ':)'
    redirect_uri = 'http://localhost:7777/callback'
    scope = 'user-library-read'
    global token
    token = util.prompt_for_user_token(username=username, 
                                    scope=scope, 
                                    client_id=client_id,   
                                    client_secret=client_secret,     
                                    redirect_uri=redirect_uri)
def get_ids():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + token,
    }
    spotify_songs = []
    offset = 0
    while offset < 7:
        loaded_songs = requests.get('https://api.spotify.com/v1/me/tracks?limit=50&offset=' + str(offset), headers=headers)
        song_list = []
        for song in range(len(loaded_songs.json()["items"])):
            song_list.append(loaded_songs.json()["items"][song]["track"]["id"])

        song_list
        spotify_songs.append(song_list)
        offset = offset +1
    if offset == 7:
        loaded_songs = requests.get('https://api.spotify.com/v1/me/tracks?limit=7&offset=' + str(offset), headers=headers)
        song_list = []
        for song in range(len(loaded_songs.json()["items"])):
            song_list.append(loaded_songs.json()["items"][song]["track"]["id"])

        song_list
        spotify_songs.append(song_list)
    spotify_songs
    flat_spotify_songs  = sum((spotify_songs), [])

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    offset2 = 0
    not_liked_list = []
    while offset2 < 17:
        not_liked_playlist = requests.get('https://api.spotify.com/v1/playlists/0l6KZUCPhG7ypHHBGhXb5s/tracks?limit=50', headers=headers)
        not_liked_playlist.json()
        for song in range(len(not_liked_playlist.json()["items"])):
            not_liked_list.append(not_liked_playlist.json()["items"][song]["track"]["id"])   
        offset2 = offset2+1
        
    not_liked_list



    df_liked = pd.DataFrame(flat_spotify_songs, columns = ["id"])
    df_liked["liked"] = 1
    df_not_liked = pd.DataFrame(not_liked_list, columns = ["id"])
    df_not_liked["liked"] = 0
    global df
    df = pd.concat([df_liked, df_not_liked])
    df = df.sample(frac=1).reset_index(drop=True)
    return(df)

def get_features():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    #df["danceability"] = requests.get('https://api.spotify.com/v1/audio-features/'+df["id"], headers=headers).json()#["danceability"]

    for index, row in df.iterrows():
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



scrape_preload()
get_ids()
get_features()

df


test_song_id = '7jEyX4bqaCSdMN4D4JNnVj'
"""
#TEST INDIVIDUÁLNÍ PÍSNĚ
test_song_id = '7jEyX4bqaCSdMN4D4JNnVj'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

testsong = requests.get('https://api.spotify.com/v1/tracks/'+test_song_id, headers=headers)
testsong.json()
"""

"""
#TEST ČÍSLA PLAYLISTU
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

test_playlist = requests.get('https://api.spotify.com/v1/playlists/0l6KZUCPhG7ypHHBGhXb5s/tracks?limit=50', headers=headers)

test_playlist.json()
"""

"""
#test features
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

test_features = requests.get('https://api.spotify.com/v1/audio-features/'+test_song_id, headers=headers)

test_features.json()
"""
