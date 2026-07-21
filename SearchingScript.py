import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from sklearn.preprocessing import MinMaxScaler as MM_scale
import math
#from sklearn.feature_extraction.text import TfidfVectorizer

#----------------------------------------------
# Step 1: Creating and Reforming DataFrame
#----------------------------------------------
#reforming data set for more flexibility for future
df = pd.read_csv('spotify_dataset.csv')
song_text_df = pd.read_csv('spotify_millsongdata.csv').drop(columns=['link'])
df_for_similarity_algo = df.drop(['Unnamed: 0','track_id','track_genre','artists','album_name','track_name','explicit','duration_ms','time_signature'],axis=1).apply(pd.to_numeric)
df_for_work_with_track = df.drop(['Unnamed: 0','track_id','time_signature','duration_ms','popularity'],axis=1)
#df_for_search = df.drop(['Unnamed: 0', 'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
#                        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
#                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature',
#                        'track_genre'],axis=1)
#df_for_search = df_for_search['track_name'].str.lower()
track_genre = df['track_genre']

# - Vectorizing for all texts
#vectorizer = TfidfVectorizer(stop_words='english')
#tfidf_matrix = vectorizer.fit_transform(song_text_df['text'].fillna(''))

scaler = MM_scale()
scaled_df = scaler.fit_transform(df_for_similarity_algo)
scaled_df = pd.DataFrame(scaled_df, columns=df_for_similarity_algo.columns, index=df_for_similarity_algo.index)
#--------------------------------------------------------------
# Step 2: Searching row with characteristics for current song
#--------------------------------------------------------------

def Get_User_Input():  # - Collect Song name or a text from song
    user_request =  input('Give us a song name to search: ')
    return user_request

def find_track(track_name):
    character_data = []
    track_name = track_name.lower()

    # Clear data_list from rows withou current song name

    data_list = df_for_work_with_track[df_for_work_with_track['track_name'].str.contains(track_name,regex=False,case=False)]
    if data_list.dropna().empty:
        print('Error!')
    for index, row in data_list.iterrows():
        character_data.append(row['artists'])
    character_data = set(character_data)
    character_data = list(character_data)

    # - User choose a correct artist
    for index, i in enumerate(character_data):
        print(index+1, i)
    if len(character_data) > 1:
        print('We found some artists with similar song name! Please choose what artist do you mean: ')
        artist_user_chose = character_data[int(input(f'Select an artist: from 1-{len(character_data)}: ')) - 1]
        print(f'{artist_user_chose} --- {track_name}')

    # - Search by artist name

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

#-----------------------------------------
#   TF-IDF algorithm
#-----------------------------------------

# tf(word,blob):
    #return blob.words.count(word)

#def n_containing(word, bloblist):
    #return sum(1 for blob in bloblist if word in blob.words)

#def idf(word, bloblist):
    #return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

#def tfidf(word, blob ,bloblist):
    #return tf(word, blob)  * idf(word,bloblist)



#def find_track_textv(input_text):
    ### - Old TF-IDF script (takes (O(n*m) times)
    # from textblob import TextBlob as tb
    #
    # input_text = input_text.lower()
    # words = input_text.split()
    #
    # mask = song_text_df['text'].str.contains('|'.join(words), case=False,na=False)
    # filtered_df = song_text_df[mask]
    #
    # if filtered_df.dropna().empty:
    #     print("No songs with this words")
    #     return None
    #
    # if len(words) == 0:
    #     print('No words to search')
    #     return None
    #
    # bloblist = [tb(text) for text in filtered_df['text'].fillna('')]
    #
    # best_score = -1
    # best_index = None
    #
    # for idx, blob in enumerate(bloblist):
    #     score = 0
    #     for word in words:
    #         score += tfidf(word,blob,bloblist)
    #     if score > best_score:
    #         best_score = score
    #         best_index = idx
    #
    # if best_score is not None:
    #     print(f"Best match found: {filtered_df.iloc[best_index]['song']}")
    #     return df_for_similarity_algo.loc[best_index]
    # else:
    #     print("No song found")
    #     return None
    #input_tfidf = vectorizer.transform([input_text])
    #scores = (tfidf_matrix * input_tfidf.T).toarray().flatten()
    #best_index = scores.argmax()
    #return df_for_similarity_algo.loc[best_index]

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
track_row = find_track(Get_User_Input())
#text_row = None

#if len(user_input) < 25:
    #track_row = find_track(user_input)
#else:
    #text_row = find_track_textv(user_input)

if track_row is not None:
    Song_index_list = []
    for index, value in find_similar_song(track_row).items():
        Song_index_list.append(index)
    Result_list = []
    for index in Song_index_list:
        Result_list.append(df_for_work_with_track['track_name'].loc[index])
    print(*Result_list, sep=' , ')
# - - - - - - - - - - - - - - - - - - - - - - - - - - -
