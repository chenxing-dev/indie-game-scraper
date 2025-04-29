from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Game(BaseModel):
    title: str
    developer: str
    url: str
    published_date: str
    price: str
    tags: list[str]

@app.post("/games/")
async def create_game(game: Game):
    # Add database insertion logic here
    return {"status": "success", "id": game.url}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)