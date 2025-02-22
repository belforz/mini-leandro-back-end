import pytest
from fakeredis import FakeRedis
from app.services.redis_service import RedisService
from app.config.connectors.redis_connector import redis_connector
import json

#Esse é um teste mockado

@pytest.fixture
def mock_redis(monkeypatch):
    fake_redis = FakeRedis(decode_responses=True)
    monkeypatch.setattr(redis_connector, "redis_client", fake_redis)
    fake_redis.flushall()  
    return fake_redis

def test_save_interaction(mock_redis):
    user_id = "user123"
    message = "Olá"
    response = "Oi! Como posso ajudar?"
    
    RedisService.save_interaction(user_id, message, response)
    
    interactions = mock_redis.lrange(f"user:{user_id}:interactions", 0, -1)
    assert len(interactions) == 1
    
   
    saved_interaction = json.loads(interactions[0])
    assert saved_interaction["message"] == message 
    assert saved_interaction["response"] == response
    
def test_interaction_limit(mock_redis):
    user_id = "user456"
    for i in range(105): 
        RedisService.save_interaction(user_id, f"Msg {i}", f"Resposta {i}")
    
    interactions = mock_redis.llen(f"user:{user_id}:interactions")
    assert interactions == 100  