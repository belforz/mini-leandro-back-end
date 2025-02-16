import pytest
from mongomock import MongoClient
from app.core.connectors.mongo import MongoConnector


@pytest.fixture(scope="function")
def mongo_connector(mocker):
    """
    Mocka a conexão com o MongoDB usando mongomock.
    """
    mocker.patch("app.core.connectors.mongo.MongoClient", side_effect=MongoClient)
    mongo_connector = MongoConnector(mongo_uri="mongodb://mockserver:27017/minibot")
    return mongo_connector

def test_connector_should_initialize_and_close(mongo_connector):
    """
    Testa se o conector é inicializado corretamente e se fecha sem erros.
    """
    mongo_connector.connect()
    assert mongo_connector.connection is not None
    assert isinstance(mongo_connector.connection, MongoClient)

    mongo_connector.close()

def test_get_connector_should_return(mongo_connector):
    """
    Testa se o conector retorna a conexão corretamente.
    """
    mongo_connector.connect()
    connector = mongo_connector.db
    assert connector is not None

def test_get_connector_should_not_return(mongo_connector):
    """
    Testa se o conector levanta um erro ao tentar acessar sem inicializar.
    """
    mongo_connector.close()
    with pytest.raises(AttributeError):
        _ = mongo_connector.db
