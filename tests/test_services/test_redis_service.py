import pytest
from app.services.redis_service import RedisService

#Esse é um teste real

@pytest.fixture(autouse=True)
def clean_redis():
    RedisService.clear_interactions()
    yield
    RedisService.clear_interactions()

def test_save_interaction():
    message = "Olá, como vai você?"
    response = "Estou bem, obrigado!"
    
    RedisService.save_interaction(message, response)
    
    interactions = RedisService.get_recent_interactions(1)
    assert len(interactions) == 1
    assert interactions[0]["message"] == message  
    assert interactions[0]["response"] == response

def test_interaction_limit():
 
    for i in range(105):
        RedisService.save_interaction(f"Mensagem {i}", f"Resposta {i}")
    
    interactions = RedisService.get_recent_interactions(100)
    assert len(interactions) == 100  