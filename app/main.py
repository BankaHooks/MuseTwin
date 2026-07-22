from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
#from SearchingScript import *

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse('main.html')

@app.get("/health")
def health():
    return Response(status_code=200)
