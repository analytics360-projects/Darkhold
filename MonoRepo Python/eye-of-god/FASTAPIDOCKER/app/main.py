from bs4 import BeautifulSoup
import requests
import json
from fastapi import FastAPI
from datetime import datetime

x = datetime.now()

app = FastAPI()

@app.get('/{full_path:path}')
def pred_image(full_path: str):
    try:
        print(full_path)
        page = requests.get(full_path)
        soup = BeautifulSoup(page.content , 'lxml')
        soupon = str(soup.prettify().encode('utf-8'))  
        JsonData = str(x)  + str(json.dumps(soupon))
        print(JsonData)
        return JsonData
    except:
        return "Error en el minado"