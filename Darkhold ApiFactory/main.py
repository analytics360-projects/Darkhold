import requests
from fastapi import FastAPI
import json

app = FastAPI()


@app.post('/')   
def Parlamentar(ReqType, Body:object | None = None, Url: str | None = None, Headers: dict | None = None):
    match ReqType:
        case "get":
            r = requests.get(Url,headers=Headers,data=Body) 
            print(r,r.headers,r.text)
            return r.text
        case "post":
            r = requests.post(Url,headers=Headers,data=Body) 
            print(r,r.headers,r.text)
            return r.text
        case "patch":
            return("No implementado, contactar a la casa blanca")

        case "delete":
            return("delete")

        case "put":
            return("No implementado, contactar a la casa blanca")
        case _:
            return("Error: No se encontro Tipo de peticion")
