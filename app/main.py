from fastapi import FastAPI
from app.config.connectors.mongo import MongoConnector
from app.routes.chatbot import router as chatbot_router

app = FastAPI(title= "Minibot API", version ="0.0.1")

db_connector = MongoConnector()

@app.on_event("startup")
def startup_db_client():
    db_connector.connect()

@app.on_event("shutdown")
def shutdown_db_client():
    db_connector.close()

# Registrar rotas
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])

@app.get("/")
def home():
    return {"message": "Bem-vindo ao Minibot!"}