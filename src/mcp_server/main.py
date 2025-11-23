from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import os

from .config import settings
from . import db


class QueryRequest(BaseModel):
    sql: str
    params: Optional[Dict[str, Any]] = None


app = FastAPI(title="MCP FastAPI Server", version="0.1")


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tables")
async def get_tables() -> List[str]:
    try:
        return await db.list_tables()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query(request: QueryRequest) -> List[Dict[str, Any]]:
    sql = request.sql.strip()
    if not sql.lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries allowed on /query")
    try:
        rows = await db.run_read_query(sql, request.params)
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/execute")
async def execute(request: QueryRequest) -> Dict[str, Any]:
    if not settings.ALLOW_WRITE:
        raise HTTPException(status_code=403, detail="Write operations are disabled (ALLOW_WRITE=false)")
    try:
        result = await db.run_write_query(request.sql, request.params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = settings.PORT
    uvicorn.run("src.mcp_server.main:app", host="0.0.0.0", port=port, reload=True)
