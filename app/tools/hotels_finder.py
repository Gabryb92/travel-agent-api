import os
from langchain_core.tools import tool
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Optional
from enum import IntEnum

load_dotenv()

#Classe enumerata per le classificazioni degli hotel (da 2 a 5 stelle)
class HotelClassEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

#modello di input che definisce e valida i parametri di ricerca:
# località hotel, data check-in e check-out, numero adulti e bambini, classe hotel
class HotelsInput(BaseModel):
    q: str = Field(description="Location of the hotel")
    check_in_date: str = Field(description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13.")
    check_out_date: str = Field(description="The return date (YYYY-MM-DD) e.g. 2024-12-19.")
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")
    hotel_class: Optional[int] = Field(2, description="The hotel class avaible from 2 to 5 .Defaults to 2.")
    
class HotelsInputSchema(BaseModel):
    params : HotelsInput

#Funzione che elabora la richiesta e interagisce con l'API, quando viene chiamta prende i parametri forniti e costruisce una query appropriata per SerpAPI vengono restituiti in italiano i risultati e la valuta in Euro e restituisce 5 risultati.
#E' stata dichiarata come tool per rendendola ideale per l'integrazione in applicazioni di automazione e chatbot
@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.
    
    Parameters:
        q (str): Location of the hotel.
        check_in_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
        check_out_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
        adults (int): The number of adults. Defaults to 1.
        children (int): The number of children. Defaults to 0.
        hotel_class (int): The hotel class available from 2 to 5. Defaults to 2.
    
    Returns:
        dict: A dictionary containing the hotels info. If the API call fails, it returns the
error message as a string.
    
    """   
    
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine" : "google_hotels",
        "hl" : "it",
        "gl" : "it",
        "currency" : "EUR",
        "q" : params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults" : params.adults,
        "children" : params.children,
        "hotel_class": params.hotel_class,
        "num" : 5
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()["properties"]
       
    except Exception as e:
        print(f"Error: {e}")
        return str(e)
    
    # Tracing
    print("*" * 80)
    print("hotels_finder")
    print("*" * 80)
    return results