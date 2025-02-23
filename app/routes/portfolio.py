from fastapi import APIRouter, HTTPException
from app.services.portfolio_service import PortfolioService
from app.models.portfolio import PortfolioSection

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])
portfolio_service = PortfolioService()

@router.get("/{section}", response_model=PortfolioSection)
def get_section(section: str):
    section_data = portfolio_service.get_section(section)
    if not section_data:
        section_data = portfolio_service.generate_section(section)
        if not section_data:
            raise HTTPException(status_code=404, detail=f"Seção '{section}' não encontrada e não pôde ser gerada.")
    return section_data

@router.post("/", response_model=PortfolioSection)
def create_section(section: PortfolioSection):
    result = portfolio_service.save_section(section)
    return section

@router.put("/{section}", response_model=str)
def update_section(section: str, data: dict):
    result = portfolio_service.update_section(section, data)
    if not result:
        raise HTTPException(status_code=404, detail=f"Seção '{section}' não encontrada.")
    return result

@router.delete("/{section}", response_model=bool)
def delete_section(section: str):
    result = portfolio_service.delete_section(section)
    if not result:
        raise HTTPException(status_code=404, detail=f"Seção '{section}' não encontrada.")
    return result