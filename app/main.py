from fastapi import FastAPI
from app.config.connectors.mongo import MongoConnector
from app.routes.chatbot import router as chatbot_router
from app.routes.portfolio import router as portfolio_router

app = FastAPI(
    title="Assistente de Portfolio API",
    version="0.0.2",
    description="Assistente de Inteligencia Artificial Generativo para gerenciar e interagir com seu portfolio",
    contact={
        "name": "Leandro",
        "email": "maceodobeiramar@hotmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

db_connector = MongoConnector()

@app.on_event("startup")
def startup_db_client():
    """Conecta ao MongoDB quando a aplicação inicia."""
    db_connector.connect()
    print("Conectado ao MongoDB.")

@app.on_event("shutdown")
def shutdown_db_client():
    """Fecha a conexão com o MongoDB quando a aplicação é encerrada."""
    db_connector.close()
    print("Conexão com o MongoDB fechada.")

# Registrar rotas
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(portfolio_router, prefix="/portfolio", tags=["Portfolio"])

# Rota raiz
@app.get("/", tags=["Home"])
def home():
    """Rota raiz que retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo ao Assistente de Portfólio!"}