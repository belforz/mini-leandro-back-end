from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisConnector:
    def __init__(self):
        self.redis_client = None

    def connect(self):
        if self.redis_client is None:
            redis_url = os.getenv("UPSTASH_REDIS_REST_URL").replace("redis://", "rediss://")
            redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

            self.redis_client = Redis.from_url(
                redis_url,
                password=redis_token,
                decode_responses=True,
                ssl_cert_reqs=None  
            )

    def get_client(self):
        if not self.redis_client:
            self.connect()
        return self.redis_client

redis_connector = RedisConnector()