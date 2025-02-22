import pytest
from mongomock import MongoClient
from app.config.connectors.mongo import MongoConnector
from app.models.interaction import InteractionModel
from app.models.tokens import TokenModel
from app.models.statistics import StatisticsModel

@pytest.fixture(scope="function")
def mongo_connector():
    mongo_client = MongoClient()  
    db = mongo_client["minibot"]
    return db

def test_interaction_collection_creation(mongo_connector):
    interaction = InteractionModel(message="Hello, bot!", response="Hello, user!")
    mongo_connector["interactions"].insert_one(interaction.model_dump())  

def test_token_collection_creation(mongo_connector):
    token = TokenModel()
    mongo_connector["tokens"].insert_one(token.model_dump())  

def test_statistics_collection_creation(mongo_connector):
    statistics = StatisticsModel(total_messages=10, most_used_words={"hello": 5})
    mongo_connector["statistics"].insert_one(statistics.model_dump())  
