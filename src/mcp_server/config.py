import os
from typing import Optional


class Settings:
    DATABASE_URL: Optional[str]
    ALLOW_WRITE: bool
    PORT: int

    def __init__(self) -> None:
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.ALLOW_WRITE = os.getenv("ALLOW_WRITE", "false").lower() in ("1", "true", "yes")
        try:
            self.PORT = int(os.getenv("PORT", "8000"))
        except ValueError:
            self.PORT = 8000


settings = Settings()
