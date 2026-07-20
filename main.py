from fastapi import FastAPI
from SearchingScript import *
from TFIDF import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test Sever Start"}