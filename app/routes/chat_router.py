from fastapi import APIRouter
from pydantic import BaseModel
from services import Agent

#istanza per il router
router = APIRouter()

class ChatCompletionRequest(BaseModel):
    
    #Il field messages conterrà la lista dei messaggi che compongono la conversazione
    messages: list
    
    model_config = {
        "json_schema_extra" : {
            "example" : {
                "messages" : [
                    {
                        "role" : "user",
                        "content" : "Vorrei organizzare un viaggio a Roma"
                    }
                ]
            }
        }
    }

@router.post("/travel-agent") #Definizione dell'endpoint POST per il travel agent
def chat_completion(request: ChatCompletionRequest):
    """
    EndPoint per la gestione delle richieste di chat.
    Processa i messaggi ricevuti e restituisce una risposta dall'agente di viaggio
    
    Args:
        request (ChatCompletionRequest): La richiesta contenente i messaggi della conversazione
    Returns:
        dict: La risposta elaborata dall'agente di viaggio
    Raises:
        HTTPException: In caso di errori durante l'elaborazione della richiesta
    """
    #Creazione di una nuova istanza dell'agente
    agent = Agent() 
    
    #Elaborazione dei messaggi e generazione della risposta
    response = agent.run(messages=request.messages)
    
    # Tracing
    print("*" * 80)
    print("chat_completion")
    print("*" * 80)
    # print("request messages: ", request.messages)
    # print("response: ", response)
    # Restituzione della risposta
    return response
        