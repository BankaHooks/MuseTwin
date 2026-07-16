import pandas as pd
#import numpy as np - don`t need rn

#----------------------------------------------
# Step 1: Creating and Reforming DataFrame
#----------------------------------------------
#reforming data set for more flexibility for future
df = pd.DataFrame(pd.read_csv('spotify_dataset.csv'))
df_for_similarity_algo = df.drop(['Unnamed: 0','time_signature','track_genre','duration_ms','artists','popularity','track_id','track_name','album_name','key','mode','explicit'],axis=1).apply(pd.to_numeric)
df_for_work_with_track = df.drop(['Unnamed: 0','track_id','time_signature','duration_ms','popularity'],axis=1)
df_for_search = df.drop(['Unnamed: 0', 'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
                        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature',
                        'track_genre'],axis=1)
df_for_search = df_for_search['track_name'].str.lower()

#--------------------------------------------------------------
# Step 2: Searching row with characteristics for current song
#--------------------------------------------------------------

def find_track(track_name):
    character_data = []
    track_name = track_name.lower()
    data_list = df_for_work_with_track[df_for_work_with_track['track_name'].str.contains(track_name,regex=False)]
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
        print(data_list.columns)
        return df_for_similarity_algo.loc[data_list.index]
    elif len(character_data) == 1:
        artist_user_chose = character_data[0]
        print(f'{artist_user_chose} --- {track_name}')
        data_list = data_list[(data_list['artists'].str.lower() == artist_user_chose.lower())]
        return df_for_similarity_algo.loc[data_list.index]
    else:
        print("Ooops, it`s look like we didn`t found this song!... Sorry")
        return None



def find_important_data(track_name):
    for columns in df_for_similarity_algo:
        print(columns)

def GetUser_TrackName():
    TrackName = input('Make sure track name is correct!!!: ')
    return TrackName


track = find_track(GetUser_TrackName())
#find_important_data(1)
print(track)
print(df_for_similarity_algo.shape)

# noinspection PyTypeChecker
# - Just for Analyze
#print(df.columns)
# print()
# # noinspection PyTypeChecker
# print(df_for_similarity_algo.columns)
# print()
# # noinspection PyTypeChecker
# print(df_for_work_with_track.columns)
# print()

