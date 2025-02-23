import json
from datetime import datetime, UTC
from typing import Optional
from app.config.connectors.mongo import MongoConnector
from app.config.connectors.redis_connector import RedisConnector
from app.models.portfolio import PortfolioSection
from app.config.connectors.deep_seek_connector import DeepSeekConnector

class PortfolioService:
    def __init__(self):
        self.db_connector = MongoConnector()
        self.db_connector.connect()
        self.collection = self.db_connector.db["mini-bot"]
        self.redis_connector = RedisConnector()
        self.redis_client = self.redis_connector.get_client()
        self.TTL = 3600  # 1 hora em segundos
        self.deepseek = DeepSeekConnector()

    def save_section(self, data: PortfolioSection) -> str:
        data_dict = data.model_dump()
        data_dict["last_updated"] = data_dict["last_updated"].isoformat()
        self.collection.update_one(
            {"section": data.section},
            {"$set": data_dict},
            upsert=True
        )
        self.redis_client.setex(f"portfolio:{data.section}", self.TTL, json.dumps(data_dict))
        return f"Seção '{data.section}' salva com sucesso."

    def get_section(self, section: str) -> Optional[PortfolioSection]:
        cached_data = self.redis_client.get(f"portfolio:{section}")
        if cached_data:
            return PortfolioSection(**json.loads(cached_data))
        
        section_data = self.collection.find_one({"section": section}, {"_id": 0})
        if section_data:
            self.redis_client.setex(f"portfolio:{section}", self.TTL, json.dumps(section_data))
            return PortfolioSection(**section_data)
        return None

    def generate_section(self, section: str) -> Optional[PortfolioSection]:
        try:
            response = self.deepseek.send_message([
                {"role": "system", "content": "Você é um assistente de portfólio. Seja conciso."},
                {"role": "user", "content": f"Resuma a seção '{section}' em até 150 palavras."}
            ], max_tokens=200)
            
            if response:
                section_data = {
                    "title": section.capitalize(),
                    "section": section,
                    "content": [response.strip()],
                    "last_updated": datetime.now(UTC).isoformat()
                }
                self.save_section(PortfolioSection(**section_data))
                return PortfolioSection(**section_data)
        except Exception as e:
            print(f"Erro ao acessar DeepSeek API: {e}")
            return None

    def update_section(self, section: str, data: dict) -> str:
        existing_section = self.collection.find_one({"section": section}, {"_id": 0})
        if not existing_section:
            return None

        if "last_updated" in existing_section:
            existing_section["last_updated"] = datetime.fromisoformat(existing_section["last_updated"])
        
        existing_section.update(data)
        existing_section["last_updated"] = datetime.now(UTC)
        
        try:
            updated_data = PortfolioSection(**existing_section).model_dump()
            updated_data["last_updated"] = updated_data["last_updated"].isoformat()
        except Exception as e:
            return f"Erro de validação: {e}"

        updated = self.collection.find_one_and_update(
            {"section": section},
            {"$set": updated_data},
            return_document=True,
            projection={"_id": 0}
        )
        
        if updated:
            self.redis_client.setex(f"portfolio:{section}", self.TTL, json.dumps(updated))
            return f"Seção '{section}' atualizada com sucesso."
        return None

    def delete_section(self, section: str) -> bool:
        try:
            deleted = self.collection.delete_one({"section": section})
            if deleted.deleted_count > 0:
                self.redis_client.delete(f"portfolio:{section}")
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar seção: {e}")
            return False