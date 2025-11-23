from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy import text
from sqlalchemy import inspect
from .config import settings

engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global engine
    if engine is None:
        if not settings.DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set")
        engine = create_async_engine(settings.DATABASE_URL, future=True)
    return engine


async def list_tables() -> List[str]:
    eng = get_engine()
    async with eng.connect() as conn:
        def _inspector(sync_conn):
            insp = inspect(sync_conn)
            return insp.get_table_names()

        tables = await conn.run_sync(_inspector)
        return tables


async def run_read_query(sql: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    eng = get_engine()
    async with eng.connect() as conn:
        result = await conn.execute(text(sql), params or {})
        rows = result.mappings().all()
        return [dict(r) for r in rows]


async def run_write_query(sql: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    eng = get_engine()
    async with eng.begin() as conn:
        result = await conn.execute(text(sql), params or {})
        try:
            affected = result.rowcount
        except Exception:
            affected = -1
        return {"rowcount": affected}
