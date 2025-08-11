# Copilot Positions Demo

A minimal API + OpenAPI connector you can import into **Microsoft Copilot Studio** as an action. The action returns a position by ticker (e.g., `AAPL`). Start with a local stub DB, then flip an env var to use **Azure SQL**.

## Quickstart (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adjust values if needed
uvicorn api.main:app --reload