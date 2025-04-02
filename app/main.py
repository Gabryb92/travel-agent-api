# Questa riga importa la classe FastAPI dal framework FastAPI. È l'elemento principale necessario per creare un'applicazione web API.
from fastapi import FastAPI

# Qui viene importato un router chiamato `chat_router` da un modulo locale (file) `app.routes`. I router in FastAPI sono utilizzati per organizzare le diverse route (endpoint) dell'API in modo modulare.
from routes import chat_router

# Questa riga importa il middleware CORS (Cross-Origin Resource Sharing). CORS è un meccanismo di sicurezza che consente o blocca le richieste da domini diversi da quello dell'API.
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

# Qui viene creata un'istanza dell'applicazione FastAPI. Questo oggetto `app` sarà il punto principale dell'applicazione dove verranno registrate tutte le route e i middleware.

app = FastAPI()

#In origins mettiamo tutti i domini permessi per effettuare chiamate api

# origins = [
#     "http://127.0.0.1:8000" # Frontend 
#     "http://localhost:8000" #Alias localhost
# ]

origins = os.getenv("CORS_ORIGINS", "").split(",")

#Configurazione middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins, #Domini permessi
    allow_credentials = True, #Invio credenziali
    allow_methods = ["*"], # Permessi per metodi HTTP (GET,POST...)
    allow_headers = ["*"]  # Permessi per gli headers (application/json, ecc)
)

#Configurazione del router
app.include_router(
    chat_router.router, #Router definito nel file chat_router
    tags=["Chat"], #Tag per la documentazione Swagger
    prefix="/chat", #Prefisso per tutte le route del router
)


