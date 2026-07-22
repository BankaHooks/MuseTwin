from email import message

from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from app.SearchingScript import find_track

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/search")
def search(track_name: str):
    result = find_track(track_name)
    return {"result": result}

@app.get("/health")
def health():
    return Response(status_code=200)
