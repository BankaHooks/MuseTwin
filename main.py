from fastapi import FastAPI
from SearchingScript import *
from TFIDF import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test Sever Start"}

@app.get("/search")
def search_song(track_name: str):
    # my logics
    track_row = find_track(track_name)
    if track_row is not None:
        similar = find_similar_song(track_row)
        return {f'Similar songs: {similar}'}
    return {'Error: "Incorrect song_name"'}