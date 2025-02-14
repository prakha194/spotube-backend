from fastapi import FastAPI
import requests

app = FastAPI()

import os
YT_API_KEY = os.getenv("YT_API_KEY")

@app.get("/")
def home():
    return {"message": "Spotube Backend Running"}

@app.get("/trending")
def get_trending():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&chart=mostPopular&regionCode=IN&key={YT_API_KEY}"
    response = requests.get(url)
    return response.json()
