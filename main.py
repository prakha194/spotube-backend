from fastapi import FastAPI
import requests
import os

app = FastAPI()

# 1. Get YouTube API Key from environment variables (Corrected name)
YT_API_KEY = os.getenv("YT_API_KEY")  # Use the correct name: YT_API_KEY
if not YT_API_KEY:
    raise ValueError("Missing YT_API_KEY environment variable")

# ... (rest of the code is the same as the previous corrected version)
# ... (including the /videos and /trending routes)