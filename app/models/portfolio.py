from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from typing import List, Optional

class PortfolioSection(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "section": "experience",
                "title": "Experiência Profissional",
                "content": [
                    "Desenvolvedor Backend na Empresa X",
                    "Engenheiro de IA na Startup Y"
                ],
                "last_updated": "2025-02-22T10:00:00Z"
            }
        }
    )

    section: str = Field(..., title="Nome da seção", examples=["Habilidades"])
    title: Optional[str] = Field(default=None, title="Título da seção", examples=["Skills"])
    content: List[str] = Field(..., title="Conteúdo da seção", examples=[["Python", "JavaScript", "PHP"]])
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC), title="Última atualização")