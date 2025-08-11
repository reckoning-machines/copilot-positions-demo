import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from opencensus.ext.azure.log_exporter import AzureLogHandler

from .db import Position, use_stub, get_stub_position, get_sql_position

load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("positions")
if (cs := os.getenv("APPINSIGHTS_CONNECTION_STRING")):
    logger.addHandler(AzureLogHandler(connection_string=cs))

app = FastAPI(title="Positions API", version="0.1.0")

class PositionOut(BaseModel):
    ticker: str
    quantity: float
    avg_price: float

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/positions/{ticker}", response_model=PositionOut)
def get_position(ticker: str):
    logger.info("positions.request", extra={"ticker": ticker})
    try:
        pos: Position | None
        if use_stub():
            pos = get_stub_position(ticker)
        else:
            pos = get_sql_position(ticker)
        if not pos:
            pos = Position(ticker.upper(), 0.0, 0.0)
        logger.info("positions.response", extra={"ticker": pos.ticker, "qty": pos.quantity})
        return PositionOut(**pos.__dict__)
    except Exception as e:
        logger.exception("positions.error")
        raise HTTPException(status_code=500, detail=str(e))