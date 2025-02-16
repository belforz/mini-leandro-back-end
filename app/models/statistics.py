from datetime import datetime, UTC
from typing import Annotated
from pydantic import BaseModel, Field

class StatisticsModel(BaseModel):
    total_messages: int
    most_used_words: dict
    last_access: Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
