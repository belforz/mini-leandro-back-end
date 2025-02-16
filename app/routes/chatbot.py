from fastapi import APIRouter, HTTPException
from app.config.connectors.mongo import MongoConnector
from pydantic import BaseModel
from typing import List

router = APIRouter()
db_connector = MongoConnector()

class MongoDBStatusResponse(BaseModel):
    message: str
    collections: List[str]

@router.get("/chat", response_model=MongoDBStatusResponse)
def test_db():
    try:
        db_connector.connect()
        collections = db_connector.db.list_collection_names()
        return {"message": "Conexão com o MongoDB funcionando!", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Erro ao conectar ao MongoDB: {str(e)}"})
