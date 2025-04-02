import os
import logging
# Questa riga importa la classe FastAPI dal framework FastAPI. È l'elemento principale necessario per creare un'applicazione web API.
from fastapi import FastAPI

# Qui viene importato un router chiamato `chat_router` da un modulo locale (file) `app.routes`. I router in FastAPI sono utilizzati per organizzare le diverse route (endpoint) dell'API in modo modulare.
from app.routes import chat_router

# Questa riga importa il middleware CORS (Cross-Origin Resource Sharing). CORS è un meccanismo di sicurezza che consente o blocca le richieste da domini diversi da quello dell'API.
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv,find_dotenv


load_dotenv()


# Configura il logging se vuoi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carica le variabili d'ambiente
dotenv_path = find_dotenv() # Trova automaticamente il .env
logger.info(f"Percorso .env trovato: {dotenv_path}")
loaded = load_dotenv(dotenv_path=dotenv_path, verbose=True) # verbose=True può dare più info
logger.info(f".env caricato: {loaded}")

# Stampa di Debug (RIMUOVI DOPO!)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    logger.info(f"DEBUG: OPENAI_API_KEY caricata: '{api_key[:5]}...{api_key[-4:]}'")
    # Verifica se ci sono virgolette residue!
    if api_key.startswith('"') or api_key.endswith('"'):
        logger.warning("ATTENZIONE: La chiave API caricata sembra contenere virgolette!")
else:
    logger.error("ERRORE: OPENAI_API_KEY non trovata nelle variabili d'ambiente!")

# Qui viene creata un'istanza dell'applicazione FastAPI. Questo oggetto `app` sarà il punto principale dell'applicazione dove verranno registrate tutte le route e i middleware.

app = FastAPI()

#In origins mettiamo tutti i domini permessi per effettuare chiamate api

# origins = [
#     "http://127.0.0.1:8000" # Frontend 
#     "http://localhost:8000" #Alias localhost
# ]

origins = os.getenv("CORS_ORIGINS", "").split(",")

print("CHIAVE:", os.getenv("OPENAI_API_KEY"))



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


