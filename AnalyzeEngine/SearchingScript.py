import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from sklearn.preprocessing import MinMaxScaler as MM_scale

#----------------------------------------------
# Step 1: Creating and Reforming DataFrame
#----------------------------------------------
#reforming data set for more flexibility for future
df = pd.DataFrame(pd.read_csv('spotify_dataset.csv'))
df_for_similarity_algo = df.drop(['Unnamed: 0','track_id','track_genre','artists','album_name','track_name','explicit','duration_ms','time_signature'],axis=1).apply(pd.to_numeric)
df_for_work_with_track = df.drop(['Unnamed: 0','track_id','time_signature','duration_ms','popularity'],axis=1)
#df_for_search = df.drop(['Unnamed: 0', 'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
#                        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
#                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature',
#                        'track_genre'],axis=1)
#df_for_search = df_for_search['track_name'].str.lower()
track_genre = df['track_genre']

scaler = MM_scale()
scaled_df = scaler.fit_transform(df_for_similarity_algo)
scaled_df = pd.DataFrame(scaled_df, columns=df_for_similarity_algo.columns, index=df_for_similarity_algo.index)
#--------------------------------------------------------------
# Step 2: Searching row with characteristics for current song
#--------------------------------------------------------------

def GetUser_TrackName():
    return input('Make sure track name is correct!!!: ')

def find_track(track_name):
    character_data = []
    track_name = track_name.lower()
    data_list = df_for_work_with_track[df_for_work_with_track['track_name'].str.contains(track_name,regex=False,case=False)]
    if data_list.dropna().empty:
        print('Error!')
    for index, row in data_list.iterrows():
        character_data.append(row['artists'])
    character_data = set(character_data)
    character_data = list(character_data)
    for index, i in enumerate(character_data):
        print(index+1, i)
    if len(character_data) > 1:
        print('We found some artists with similar song name! Please choose what artist do you mean: ')
        artist_user_chose = character_data[int(input(f'Select an artist: from 1-{len(character_data)}: ')) - 1]
        print(f'{artist_user_chose} --- {track_name}')
        data_list = data_list[(data_list['artists'].str.lower() == artist_user_chose.lower())]
        data_list = data_list.head(1)
        return df_for_similarity_algo.loc[data_list.index]
    elif len(character_data) == 1:   # - Fix this (remake by other more user-choice friendly method)
        artist_user_chose = character_data[0]
        print(f'{artist_user_chose} --- {track_name}')
        data_list = data_list[(data_list['artists'].str.lower() == artist_user_chose.lower())]
        data_list = data_list.head(1)
        return df_for_similarity_algo.loc[data_list.index]
    else:
        print("Ooops, it`s look like we didn`t found this song!... Sorry")
        return None

#------------------------------------------------------------
# Step 3: Searching for songs with similar sound (using scikit-learn)
#-------------------------------------------------------------
def find_similar_song(characteristics):
    seed_genre = df.loc[track_row.index[0] , 'track_genre']
    same_genre_mask = df['track_genre'] == seed_genre
    search_df = df_for_similarity_algo[same_genre_mask]
    filtered_scaled = scaled_df[same_genre_mask]
    scaled_characteristics = scaler.transform(characteristics)
    cos = cos_sim(scaled_characteristics,filtered_scaled.values)
    cos = cos.flatten().tolist()
    cos = pd.Series(cos, index=filtered_scaled.index).drop(track_row.index,errors='ignore')
    cos = cos.sort_values(ascending=False)
    return cos.head(5)


### - - - - - - Calling Functions[0.1V] - - - - - - -
track_row = find_track(GetUser_TrackName())
if track_row is not None:
    Song_index_list = []
    for index, value in find_similar_song(track_row).items():
        Song_index_list.append(index)
        Result_list = []
    for index in Song_index_list:
        Result_list.append(df_for_work_with_track['track_name'].loc[index])
    print(*Result_list , sep=' , ')
# - - - - - - - - - - - - - - - - - - - - - - - - - - -