from datetime import datetime, UTC
from typing import Annotated
from pydantic import BaseModel, Field

class InteractionModel(BaseModel):
    message: str
    response: str
    timestamp: Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
