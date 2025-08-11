# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Positions API")

class Position(BaseModel):
    ticker: str
    quantity: float
    avg_price: float

# stub — swap to Azure SQL later
DB = {"AAPL": Position(ticker="AAPL", quantity=120.0, avg_price=182.5)}

@app.get("/positions/{ticker}", response_model=Position)
def get_position(ticker: str):
    if ticker.upper() in DB: return DB[ticker.upper()]
    return Position(ticker=ticker.upper(), quantity=0.0, avg_price=0.0)
