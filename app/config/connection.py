import os
from pymongo import MongoClient
from dotenv import load_dotenv

#Updating env

load_dotenv()

#get URI FROM MONGO

MONGO_URI = os.getenv("MONGO_URI")

#Connection

client = MongoClient(MONGO_URI)
db = client["mini-leandro"]

#example connection

try:
    db.command("ping")
    print("✅ Conexão com o MongoDB Atlas bem-sucedida!")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")