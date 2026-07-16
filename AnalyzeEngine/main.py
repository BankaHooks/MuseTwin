import pandas as pd
#import numpy as np - don`t need rn

#----------------------------------------------
# Step 1: Creating and Reforming DataFrame
#----------------------------------------------
#reforming data set for more flexibility for future
df = pd.DataFrame(pd.read_csv('spotify_dataset.csv'))
df_for_similarity_algo = df.drop(['Unnamed: 0','time_signature','track_genre','duration_ms','artists','popularity','track_id','track_name','album_name','key','mode','explicit'],axis=1).apply(pd.to_numeric)
df_for_work_with_track = df.drop(['Unnamed: 0','time_signature','duration_ms','popularity'],axis=1)
df_for_search = df.drop(['Unnamed: 0', 'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
                        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature',
                        'track_genre'],axis=1)
df_for_search = df_for_search['track_name'].str.lower()

#--------------------------------------------------------------
# Step 2: Searching row with characteristics for current song
#--------------------------------------------------------------

def find_track(track_name):
    track_name = track_name.lower()
    data_list = df[df['track_name'].str.contains(track_name)]
    if data_list.dropna().empty:
        print('Error!')
    print(data_list)
    return data_list



def find_important_data(track_name):
    for columns in df_for_similarity_algo:
        print(columns)

def GetUser_TrackName():
    TrackName = input('Make sure track name is correct!!!: ')
    return TrackName

track = find_track(GetUser_TrackName())
find_important_data(1)


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

