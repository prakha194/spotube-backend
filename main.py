from fastapi import FastAPI
import requests

app = FastAPI()

YT_API_KEY = "AIzaSyCIZG9-3mbSsWZzpgW1K-8sVOVtSuHMvN8"

@app.get("/")
def home():
    return {"message": "Spotube Backend Running"}

@app.get("/trending")
def get_trending():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&chart=mostPopular&regionCode=IN&key={YT_API_KEY}"
    response = requests.get(url)
    return response.json()
