import os
import logging
from typing import Optional
from dataclasses import dataclass

from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

@dataclass
class Position:
    ticker: str
    quantity: float
    avg_price: float

# Simple in-memory stub for local dev
STUB_DB = {
    "AAPL": Position("AAPL", 120.0, 182.50),
    "MSFT": Position("MSFT", 80.0, 414.20),
}


def use_stub() -> bool:
    return os.getenv("USE_STUB_DB", "true").lower() == "true"


def get_stub_position(ticker: str) -> Optional[Position]:
    return STUB_DB.get(ticker.upper())


def _sqlalchemy_url() -> str:
    server = os.getenv("AZURE_SQL_SERVER")
    db = os.getenv("AZURE_SQL_DB")
    user = os.getenv("AZURE_SQL_USER")
    pwd = os.getenv("AZURE_SQL_PASSWORD")
    driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    return (
        f"mssql+pyodbc://{user}:{pwd}@{server}:1433/{db}?"
        f"driver={driver.replace(' ', '+')}&Encrypt=yes&TrustServerCertificate=no"
    )

_engine = None


def _engine():
    global _engine
    if _engine is None:
        _engine = create_engine(_sqlalchemy_url(), pool_pre_ping=True)
    return _engine


def get_sql_position(ticker: str) -> Optional[Position]:
    sql = text("""
        SELECT TOP 1 ticker, quantity, avg_price
        FROM positions
        WHERE UPPER(ticker) = UPPER(:ticker)
    """)
    with _engine().connect() as cx:
        row = cx.execute(sql, {"ticker": ticker}).fetchone()
        if not row:
            return None
        return Position(row.ticker, float(row.quantity), float(row.avg_price))