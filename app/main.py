from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel #pydantic para armar los schemas ( nos ayudan a trabajar con el body)
import uvicorn
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from app.models import Post
from . routers import post, user,auth
import asyncio


models.Base.metadata.create_all (bind=engine)

app= FastAPI()

  # Connect to an existing database
while True:
        try:
            conn = psycopg2.connect (dbname="fastapi", user="postgres", password="Maria182*", host="localhost",
                                    port=5432, cursor_factory=RealDictCursor)
            cursor=conn.cursor()
            print ("coneccion exitosa")
            break
        except Exception  as error:
            print ("coneccion a la bd fallida")
            print ("Error", error)
            time.sleep(2)
            
            
        #SECCION RUTEADORES    
#esta parte le dice donde buscar los endpoints
app.include_router(post.router) #esto le dice que vaya al file post y busque ahi los match
app.include_router(user.router) #esto le dice que vaya al file post y busque ahi los match
app.include_router(auth.router)

#MENSAJE DE PRUEBA
#----------------------------------------------------------------------------------
@app.get("/")  #este decorator lo convierte en una operation path de la api
def root(): # puede tener cualquier nombre, tratar que sea significativo
    return {"message":"Hello World2"}




