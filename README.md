# mcp-github

Repository created and pushed by assistant automation.

This repo was initialized locally and then pushed to GitHub as `mcp-github` (public).

## Notes
- Created by: assistant
- Date: 2025-11-23

## MCP FastAPI Server

This repository includes a minimal async FastAPI "MCP" server which can connect to any SQL database via a SQLAlchemy async URL provided in `DATABASE_URL`.

Files added:
- `requirements.txt` - Python dependencies
- `.env.example` - example environment variables
- `src/mcp_server/config.py` - env config
- `src/mcp_server/db.py` - SQLAlchemy async helpers
- `src/mcp_server/main.py` - FastAPI application

Quick start (local):

1. Create a virtualenv and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set environment variables (or copy `.env.example`):
```bash
export DATABASE_URL="sqlite+aiosqlite:///./mcp_example.db"
export ALLOW_WRITE=false
export PORT=8000
```

3. Run the server:
```bash
uvicorn src.mcp_server.main:app --reload --port ${PORT:-8000}
```

4. Endpoints:
- `GET /health` - health check
- `GET /tables` - list table names
- `POST /query` - run a `SELECT` query. Body: `{ "sql": "SELECT ...", "params": {}}`
- `POST /execute` - run write statements (only available if `ALLOW_WRITE=true`)

Security note: This example exposes endpoints that run raw SQL. Use strong access controls and avoid enabling write operations in public deployments without authentication and safeguards.

