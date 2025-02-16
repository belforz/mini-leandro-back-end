import logging
from pymongo import MongoClient
from app.config.base_connector import BaseDatabaseConnector
from app.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoConnector(BaseDatabaseConnector):
    def __init__(self, mongo_uri: str = None, database_name: str = "minibot"):
        super().__init__(mongo_uri or settings.MONGODB_URI, database_name)

    def connect(self):
        try:
            self.connection = MongoClient(self.db_uri)
            self.db = self.connection[self.db_name]
            self.db.command("ping")
            logger.info("✅ Conexão com o MongoDB estabelecida!")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao MongoDB: {e}")
            raise SystemExit("🚨 A API não pode rodar sem conexão com o banco de dados!")

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("🔌 Conexão com o MongoDB fechada.")
