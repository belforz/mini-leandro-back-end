import json
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.services.portfolio_service import PortfolioService
from app.models.portfolio import PortfolioSection

@pytest.fixture
def portfolio_service():
    service = PortfolioService()
    service.redis_client = MagicMock()  # Mocka o Redis
    service.collection = MagicMock()  # Mocka o MongoDB
    return service

def test_get_section_from_cache(portfolio_service):
    """Testa se a seção é recuperada do Redis quando disponível"""
    mock_section = {
        "title": "Skills",
        "section": "skills",
        "content": ["Python", "Vue.js"],
        "last_updated": datetime.now().isoformat()
    }
    portfolio_service.redis_client.get.return_value = json.dumps(mock_section)

    result = portfolio_service.get_section("skills")

    assert result is not None
    assert result.title == "Skills"
    portfolio_service.collection.find_one.assert_not_called() 
    
def test_get_section_from_mongo_when_cache_miss(portfolio_service):
    """Testa se a seção é buscada no MongoDB quando não está no Redis"""
    mock_section = {
        "title": "Projects",
        "section": "projects",
        "content": ["Chatbot AI"],
        "last_updated": datetime.now().isoformat()
    }
    portfolio_service.redis_client.get.return_value = None  
    portfolio_service.collection.find_one.return_value = mock_section

    result = portfolio_service.get_section("projects")

    assert result is not None
    assert result.title == "Projects"
    portfolio_service.redis_client.setex.assert_called_once()  

def test_get_section_not_found(portfolio_service):
    """Testa se retorna None quando a seção não existe nem no Redis nem no MongoDB"""
    portfolio_service.redis_client.get.return_value = None  
    portfolio_service.collection.find_one.return_value = None  
    result = portfolio_service.get_section("unknown")

    assert result is None
    portfolio_service.redis_client.setex.assert_not_called()  
