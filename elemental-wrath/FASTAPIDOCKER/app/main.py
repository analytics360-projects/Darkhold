from http import cookies
import numbers
from tokenize import group
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
import json
from fastapi import FastAPI
from facebook_scraper import get_posts
from facebook_scraper import get_profile
#FASTAPI FOR PARAMETERS
#GRUPOS PARA TEST 
#265882700182475
#1287986221406200
#aurora 431948614070900
app = FastAPI()
Data = []

# @app.get('/group/{group},{pages}')
# #SCRAPING APP
# def mensaje(group,pages):
#   pages = int(pages)
#   try:
#     for post in get_posts(group=group, pages=pages):
#         Data.append({"post_id": post["post_id"],
#                     "text": post['text'],
#                     "post_text": post['post_text'],
#                     "shared_text": post['shared_text'],
#                     "original_text": post['original_text'],
#                     "time": json.dumps(post['time'], default=str),
#                     "timestamp": post['timestamp'],
#                     "image": post['image'],
#                     "image_lowquality": post['image_lowquality'],
#                     "images": post['images'],
#                     "images_description": post['images_description'],
#                     "images_lowquality": post['images_lowquality'],
#                     "images_lowquality_description": post['images_lowquality_description'],
#                     "video": post['timestamp']
#                     })
#         print(Data)
#     JsonData = y = json.dumps(Data)
# #Return the JSON
#     return JsonData
#   except:
#     return JsonData

@app.get('/group/{groupId},{pages}')
def Scraper(groupId, pages):
  pages = int(pages)
  try:
    JsonData = get_posts(group=groupId  , pages=pages)
    print(JsonData)
    return JsonData
  except:
    return JsonData

    
@app.get('/profile/{account}')
def mensaje(account):
  post = get_profile(account=account)
  # for post in get_posts(post_urls=account,pages=1, cookies="cookies.txt"):
  print(post)
#Return the JSON
  return post


@app.get('/post/{post}')
def mesaje(post):
  JsonData = get_posts(post_urls=post)
  return JsonData

