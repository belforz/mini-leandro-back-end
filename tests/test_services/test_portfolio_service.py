import unittest
from datetime import datetime, UTC
from unittest.mock import patch
from app.config.connectors.mongo import MongoConnector
from app.config.connectors.redis_connector import RedisConnector
from app.models.portfolio import PortfolioSection
from app.services.portfolio_service import PortfolioService

class TestPortfolioServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_connector = MongoConnector()
        cls.mongo_connector.connect()
        cls.collection = cls.mongo_connector.db["mini-bot"]
        cls.redis_connector = RedisConnector()
        cls.redis_client = cls.redis_connector.get_client()
        cls.service = PortfolioService()

    def setUp(self):
        self.collection.delete_many({})
        self.redis_client.flushdb()

    @patch("app.config.connectors.deep_seek_connector.DeepSeekConnector.send_message")
    def test_get_section_with_deepseek_fallback(self, mock_deepseek):
        mock_deepseek.return_value = "A inteligência artificial é uma área da ciência da computação."
        section_name = "inteligencia_artificial"

        # Primeira chamada: seção não existe
        section = self.service.get_section(section_name)
        self.assertIsNone(section)

        # Gera a seção via DeepSeek
        generated_section = self.service.generate_section(section_name)
        self.assertIsNotNone(generated_section)

        # Segunda chamada: seção deve existir
        section = self.service.get_section(section_name)
        self.assertIsNotNone(section)
        self.assertEqual(section.section, section_name)
        mock_deepseek.assert_called_once()

    def test_update_section(self):
        section_data = {
            "title": "Cloud Computing",
            "section": "cloud_computing",
            "content": ["Cloud computing é a entrega de serviços de computação sob demanda."],
            "last_updated": datetime.now(UTC).isoformat()
        }
        section = PortfolioSection(**section_data)
        self.service.save_section(section)

        update_data = {"content": ["Cloud computing permite escalabilidade e flexibilidade."]}
        result = self.service.update_section("cloud_computing", update_data)
        self.assertEqual(result, "Seção 'cloud_computing' atualizada com sucesso.")

        updated_section = self.service.get_section("cloud_computing")
        self.assertEqual(updated_section.content, ["Cloud computing permite escalabilidade e flexibilidade."])

    @classmethod
    def tearDownClass(cls):
        cls.collection.delete_many({})
        cls.redis_client.flushdb()

if __name__ == "__main__":
    unittest.main()