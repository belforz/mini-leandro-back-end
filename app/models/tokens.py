from datetime import datetime, UTC
from typing import Annotated
from pydantic import BaseModel, Field

class TokenModel(BaseModel):
    used_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
