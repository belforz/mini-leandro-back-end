import json
from app.config.connectors.redis_connector import redis_connector

class RedisService:
    @staticmethod
    def save_interaction(message: str, response: str):
        """
        Salva a interação no Redis com caracteres acentuados corretamente
        e mantém um limite de 100 conversas recentes.
        """
        redis_client = redis_connector.get_client()
        interaction = json.dumps(
            {"message": message, "response": response},
            ensure_ascii=False 
        )
        redis_client.lpush("chatbot_logs", interaction)
        redis_client.ltrim("chatbot_logs", 0, 99)

    @staticmethod
    def get_recent_interactions(limit: int = 10):
        redis_client = redis_connector.get_client()
        interactions = redis_client.lrange("chatbot_logs", 0, limit - 1)
        return [json.loads(interaction) for interaction in interactions]

    @staticmethod
    def clear_interactions():
        redis_client = redis_connector.get_client()
        redis_client.delete("chatbot_logs")