import pandas as pd
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from app.SearchingScript import find_track, find_similar_song, df_for_work_with_track
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/search")
def search(track_name: str, artist: str=None):
    result = find_track(track_name, artist)

    if result is None:
        return {'error':"Track not found"}

    if isinstance(result, dict) and "multiple_matches" in result:
        return {"multiple_matches":result["multiple_matches"]}

    if isinstance(result, pd.DataFrame):
        return {'result': result.to_dict(orient='records')}

    return {"result":result}

@app.get("/recommend")
def recommend(track_name: str, artist: str=None):
    track_features = find_track(track_name, artist)

    if track_features is None:
        return {'error':"Track not found"}

    if isinstance(track_features, dict) and "multiple_matches" in track_features:
        return {"multiple_matches":track_features["multiple_matches"]}

    similar = find_similar_song(track_features)
    similar_indices = similar.index.tolist()

    similar_names = df_for_work_with_track.loc[similar_indices, 'track_name'].tolist()
    similar_artists = df_for_work_with_track.loc[similar_indices, 'artists'].tolist()

    recommendations = [
        {"track" : name, "artist" : artist}
        for name, artist in zip(similar_names, similar_artists)
    ]

    return {"recommendations: ":recommendations}

@app.get("/health")
def health():
    return Response(status_code=200)
