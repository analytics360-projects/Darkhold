import uuid

from pyravendb.custom_exceptions.exceptions import AggregateException

import app.UrlScraper as Scrapy
import requests
import json
import jsonpickle
import os
# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from typing import Any
from datetime import datetime
from facebook_scraper import get_posts
from facebook_scraper import get_profile
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from ravendb import DocumentStore
from pydantic import BaseModel, Json

# load_dotenv()

# Documentación para queries en RavenDB https://github.com/ravendb/ravendb-python-client

# RavenDB

# RavenDB
RAVENDB_URL = "http://10.19.5.41:8082/"
# RAVENDB_URL = os.getenv('RAVENDB_URL')

time_now = datetime.now()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa la conexión con RavenDB
store = DocumentStore(urls=[RAVENDB_URL], database="Sans")
store.initialize()


@app.post('/facebook/group/{group_id}')
def Scraper(group_id, pages):
    pages = int(pages)
    json_data = []
    try:
        for post in get_posts(group_id):
            json_data.append(post['text'])
            return json_data
    except:
        return json_data


@app.post('/facebook/profile/{account}')
def mensaje(account):
    post = get_profile(account=account)
    return post


@app.post('/facebook/post/{post}')
def mesaje(post):
    json_data = get_posts(post_urls=post)
    return json_data


class Carpeta(BaseModel):
    carpeta_investigacion: str
    user: str


# API para crear carpetas investigación
@app.post("/create/carpeta")
def create_research(carpeta: Carpeta):
    try:
        with store.open_session() as session:
            session.store({
                "carpeta_investigacion": carpeta.carpeta_investigacion,
                "assigned": False,
                "date": time_now,
                "user_creacion": carpeta.user
            })
        session.save_changes()
        return {"message": "Campos guardos con exito"}
    except:
        return "Error en la insercción"


class Investigacion(BaseModel):
    nombre: str
    carpeta_investigacion: int
    nombre: str
    user: str


# API para crear carpetas investigación
@app.post("/create/investigación")
def create_research(investigacion: Investigacion):
    try:
        with store.open_session() as session:
            session.store({
                "carpeta_investigacion": investigacion.carpeta_investigacion,
                "investigacion": investigacion.nombre,
                "assigned": False,
                "date": time_now,
                "user_creacion": investigacion.user
            })
        session.save_changes()
        return {"message": "Campos guardos con exito"}
    except:
        return "Error en la insercción"


class Item(BaseModel):
    full_path: str  # Url a minar
    user: str  # Usuario que realiza la petición
    nombre: str  # Nombre de la investigación
    carpeta_investigacion: str  # nombre de la carpeta de investigación
    investigacion: str  # nombre de la carpeta de investigación
    tipo_busqueda: str  # 1 = Url, 2 = Facebook, 3 = Twitter, 4 = Instagram
    status: int  # 1 = Activo, 0 = Inactivo, -1 = Eliminado
    palabras: list  # Lista de palabras claves encontradas en el texto
    # contador: int  # Contador de la cantidad de veces que se ha minado la url


@app.post('/singleurl')
def single_url(item: Item):
    try:
        page = requests.get(item.full_path)
        soup = BeautifulSoup(page.content, 'lxml')
        soupon = str(soup.prettify().encode('utf-8'))
        json_data = str(time_now) + str(json.dumps(soupon))

        # Inicializa un diccionario para almacenar el conteo de cada palabra clave
        conteo_palabras = {}

        # Contar cuántas veces aparece cada palabra clave en json_data
        for palabra in item.palabras:
            count = json_data.count(palabra)
            conteo_palabras[palabra] = count

        # Inicializa una lista para almacenar los resultados
        resultados = []

        # Crea objetos de resultado para cada palabra clave
        for palabra, coincidencias in conteo_palabras.items():
            resultado = {
                "palabra": palabra,
                "coincidencias": coincidencias
            }
            resultados.append(resultado)

        # Crea un diccionario con las claves "resultados"
        respuesta = {
            "fecha": time_now,
            "url": item.full_path,
            "resultados": resultados,
            "json_data": json_data
        }

        # if(item.contador == 0):
        #   with store.open_session() as session:
        #       session.store({
        #           "carpeta_investigacion": item.carpeta_investigacion, # Id de la carpeta de investigación
        #           "investigacion": item.investigacion, # Id del parametro de busqueda
        #           "tipo_busqueda": item.tipo_busqueda,
        #           "nombre": item.nombre,
        #           "date": time_now,
        #           "assigned": False,
        #           "status ": 1,
        #           "user_creacion": item.user,
        #           "resultados": resultados  # Almacena la lista de resultados
        #       })
        #   session.save_changes()

        # data = {
        #     "message": "Campos guardados con exito",
        #     "ok": True,
        #     "status": 200,
        #     "respuesta": respuesta
        # }
        return respuesta
    except:
        return "Error en el minado"


class ItemMultiUrl(BaseModel):
    urls: list  # Url a minar
    user: str  # Usuario que realiza la petición
    nombre: str  # Nombre de la investigación
    carpeta_investigacion: str  # nombre de la carpeta de investigación
    investigacion: str  # nombre de la carpeta de investigación
    tipo_busqueda: str  # 1 = Url, 2 = Facebook, 3 = Twitter, 4 = Instagram
    status: int  # 1 = Activo, 0 = Inactivo, -1 = Eliminado
    palabras: list  # Lista de palabras claves encontradas en el texto


"""
Example
{
  "urls": [
    "https://www.google.com/","https://www.tiempo.com.mx/seccion/local/"
  ],
  "user": "vic",
  "nombre": "Test",
  "carpeta_investigacion": "1",
  "investigacion": "5",
  "tipo_busqueda": "string",
  "status": 1,
  "palabras": [
    "tiempo","html"
  ]
}
"""


@app.post('/multiurls')
def pred_image_multi(item: ItemMultiUrl):
    try:
        # Inicializa una lista para almacenar las respuestas de cada URL
        respuestas = []

        # Itera a través de cada URL en la lista
        for url in item.urls:
            print(url)
            # Crea un objeto Item para procesar cada URL individualmente
            item_single_url = Item(
                full_path=url,
                user=item.user,
                nombre=item.nombre,
                carpeta_investigacion=item.carpeta_investigacion,
                investigacion=item.investigacion,
                tipo_busqueda=item.tipo_busqueda,
                status=item.status,
                palabras=item.palabras
            )
            print(item_single_url)

            # Llama al método /singleurl para procesar la URL
            respuesta_single_url = single_url(item_single_url)
            # Agrega la respuesta de /singleurl a la lista de respuestas
            respuestas.append(respuesta_single_url)

        with store.open_session() as session:
            session.store({
                "message": "Campos guardados con exito",
                "ok": True,
                "status": 200,
                "carpeta_investigacion": item.carpeta_investigacion,  # Id de la carpeta de investigación
                "investigacion": item.investigacion,  # Id del parametro de busqueda
                "tipo_busqueda": item.tipo_busqueda,
                "nombre": item.nombre,
                "date": time_now,
                "assigned": False,
                "status ": 1,
                "user_creacion": item.user,
                "respuestas": respuestas
            })
        session.save_changes()
        return respuestas
    except:
        return "Error en el procesamiento de múltiples URLs"


@app.get('/multiurl/Urls')
def pred_image(url: str):
    try:
        Bald = Scrapy.body_reader(Scrapy.half_full_concatenator(url, False, ''), time_now=time_now)
        json_data = json.dumps(Bald)
        return json_data
    except:
        return "Error en el minado"


@app.get('/get_by_collection_and_date/{collection}/{date}')
def get_by_collection_and_date(collection: str, date: str):
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts").contains_all("date", [date])
            results_list = [dict(result) for result in results]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


@app.get('/get_collections_by_investigacion/{investigacion}')
def get_collections_by_investigacion(investigacion: str):
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts").contains_all("investigacion", [investigacion])
            # Convertir los resultados en una lista de diccionarios
            results_list = [dict(result) for result in results]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


'''
  :description: Obtiene los documentos de una colección que contengan el mismo numero de la carpeta de investigacion en el campo "json_data"
  :param carpeta: Numero de la carpeta de investigacion
  :return: Lista de documentos
'''


@app.get('/get_collection_by_carpeta_investigacion/{carpeta}')
def get_collection_by_carpeta_investigacion(carpeta: int):
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts").contains_all("carpeta_investigacion", [carpeta])
            # Convertir los resultados en una lista de diccionarios
            results_list = [dict(result) for result in results]
            # Eliminar el campo json_data de cada documento
            for item in results_list:
                for resp in item["respuestas"]:
                    if type(resp) != str:
                        del resp["json_data"]
                del item["@metadata"]
                del item["message"]
                del item["ok"]
                del item["status"]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


class CarpetaInvestigacionCollectionById(BaseModel):
    carpetaId: str  # id de carpeta de investigacion


@app.post('/get_by_id_collection')
def get_by_id_collection(carpeta: CarpetaInvestigacionCollectionById):
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts").contains_all("Id", [carpeta.carpetaId])
            # Convertir los resultados en una lista de diccionarios
            results_list = [dict(result) for result in results]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


@app.get('/get_all')
def get_all():
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts")
            # Convertir los resultados en una lista de diccionarios
            results_list = [dict(result) for result in results]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


@app.get('/get_by_collection_and_user_creacion/{collection}/{user_creacion}')
def get_by_collection_and_user_creacion(collection: str, user_creacion: str):
    try:
        with store.open_session() as session:
            results = session.query_collection("dicts").contains_all("user_creacion", [user_creacion])
            # Convertir los resultados en una lista de diccionarios
            results_list = [dict(result) for result in results]
            return results_list
    except:
        raise HTTPException(status_code=500, detail="Error en la consulta")


@app.put('/asignar/informacion_relevante')
def edit_field(document_ids: list):
    try:
        with store.open_session() as session:
            for document_id in document_ids:
                # Obtener el documento por su ID
                doc = session.load(document_id)

                if doc is None:
                    raise HTTPException(status_code=404, detail=f"Documento con ID {document_id} no encontrado")

                # Realizar la edición del campo
                doc["assigned"] = True

                # Guardar los cambios en la sesión
                session.save_changes()

            return {"message": "Campos editados exitosamente"}
    except:
        raise HTTPException(status_code=500, detail="Error al editar los campos")


@app.post("/create/history/{subcenter}/{id_folio}")
async def create_history(subcenter: str, id_folio: int, request: Request):
    fecha = time_now
    print(fecha)

    class Historical(object):
        def __init__(self, subcentro="N/A", folio=0, data=dict, created=datetime, status=1):
            self.subcentro = subcentro
            self.folio = folio
            self.data = data
            self.created = created
            self.status = status

    try:
        historical = Historical(
            subcentro=subcenter,
            folio=id_folio,
            created=fecha,
            data=jsonpickle.decode(await request.body())
        )
        with store.open_session() as session:
            session.store(historical);
        session.save_changes()
        return {"message": "Campos guardos con exito"}
    except Exception as e:
        raise AggregateException(e)


@app.get('/get_historicals')
def get_historicals_by_origin():
    class Historical(object):
        def __init__(self, Id=str, subcentro="N/A", folio=0, data=dict, created=time_now, status=1):
            self.id = Id
            self.subcentro = subcentro
            self.folio = folio
            self.data = data
            self.created = created
            self.status = status

    try:
        with store.open_session() as session:
            query = session.query(object_type=Historical)
            # Convertir los resultados en una lista de diccionarios
            results_list = list(query)
            return results_list
    except Exception as e:
        raise AggregateException(e)
