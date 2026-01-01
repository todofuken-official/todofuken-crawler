from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

TOKENS_FILE = "config/fcm_tokens.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenModel(BaseModel):
    token: str

@app.post("/save_token")
def save_token(data: TokenModel):
    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "w") as f:
            json.dump([], f)

    with open(TOKENS_FILE, "r") as f:
        tokens = json.load(f)

    if data.token not in tokens:
        tokens.append(data.token)

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

    return {"saved": True, "token": data.token}