# mcp-github

Repository created and pushed by assistant automation.

This repo was initialized locally and then pushed to GitHub as `mcp-github` (public).

## Notes
- Created by: assistant
- Date: 2025-11-23
## MCP FastAPI Server

This repository contains a minimal async FastAPI "MCP" server that runs raw SQL against any database supported
by SQLAlchemy's async engines. The server is intentionally small so you can connect it to PostgreSQL, MySQL,
SQLite or other engines by setting `DATABASE_URL`.

Quick summary of important files
- `requirements.txt` — Python dependencies
- `.env.example` — example environment variables
- `src/mcp_server/config.py` — environment-based settings loader
- `src/mcp_server/db.py` — async SQL helpers (list tables, run queries)
- `src/mcp_server/main.py` — FastAPI application with endpoints

Local quick start
1. Create and activate a virtual environment, install deps:
```bash
cd /Users/syedraza/mcp-github
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment (see `.env.example`):
```bash
export DATABASE_URL="sqlite+aiosqlite:///./mcp_example.db"
export ALLOW_WRITE=false   # keeps /execute disabled by default
export PORT=8000
```

3. Start the server (use the virtualenv python so installed deps are visible):
```bash
.venv/bin/python3 -m uvicorn src.mcp_server.main:app --reload --port ${PORT:-8000}
```

Endpoints and examples
- `GET /health` — returns {"status":"ok"}
- `GET /tables` — returns a JSON array of table names
- `POST /query` — run readonly SELECT queries
	- Example curl (read):
		```bash
		curl -s -X POST http://localhost:8000/query \
			-H 'Content-Type: application/json' \
			-d '{"sql":"SELECT 1 AS n"}'
		```
- `POST /execute` — run write statements (only if `ALLOW_WRITE=true`)

Safety note
- This server executes raw SQL supplied via HTTP. Do not enable `ALLOW_WRITE` or expose the server
	to untrusted networks without authentication, authorization, and proper input validation.

Repository & branch
- GitHub: https://github.com/majidraza1228/mcp-github
- Current branch with server code: `syed_first`

Need help?
- I can: create a demo SQLite DB and run smoke tests, add API-key auth, create a Dockerfile, or open a PR to merge this branch into `main`.


