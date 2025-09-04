from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel #pydantic para armar los schemas ( nos ayudan a trabajar con el body)
import uvicorn
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from app.models import Post

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


     
#MENSAJE DE PRUEBA
#----------------------------------------------------------------------------------
@app.get("/")  #este decorator lo convierte en una operation path de la api
def root(): # puede tener cualquier nombre, tratar que sea significativo
    return {"message":"Hello World2"}

#MUESTRA TODOS LOS POSTS
#--------------------------------------------------------------------------------------------------------
@app.get("/posts")  #lee todos los posts
def get_posts(db: Session = Depends(get_db)):
   posts=  db.query(models.Post).all() #le decimos un query de que model especifico, recordemos que los modelos son tablas
   return {"data": posts}

 #CREA UN POST
#--------------------------------------------------------------------------------------------------------
@app.post("/createposts", status_code=status.HTTP_201_CREATED)   
def create_posts(posteo: schemas.Class_CreatePost , db: Session = Depends(get_db)): #no confundir uno es la clase post (schema) (que recibe los datos) y el otro el modelo post
    nuevo_post =  models.Post(**posteo.model_dump())
    db.add(nuevo_post)
    db.commit()
    db.refresh(nuevo_post)
    return {"mensaje": nuevo_post} 

#TRAE UN POST
#-----------------------------------------------------------#-----------------------------------------------------------
#ponerla al final para evitar que tome alguna anterior como valida
@app.get("/posts/{id}")
def buscar_post(id:int, db: Session = Depends(get_db)):  #esto valida que sea un entero
    post_encontrado=db.query(models.Post).filter(models.Post.id==id).first()
    if not post_encontrado:
        print ("no se encontro")
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"el id {id} no se encontro")
    return {"post detail": post_encontrado}

#BORRA UN POST
#-----------------------------------------------------------#-----------------------------------------------------------
@app.delete("/posts/{id}") #BORRRA UN POST
def borra_post(id:int, db: Session = Depends(get_db)):     #esto valida que sea un entero
    post_borrado=db.query(models.Post).filter(models.Post.id==id)
    #print (post_borrado)
    if post_borrado.first() is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    post_borrado.delete(synchronize_session=False)
    db.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)

#MODIFICA UN POST
#-----------------------------------------------------------#-----------------------------------------------------------
@app.put("/post/{id}")
def actualiza_post(id:int, param_post: schemas.Class_CreatePost,db: Session = Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    post_encontrado=post_query.first()
    if post_encontrado is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    post_query.update(param_post.model_dump(),synchronize_session=False)#se le pasa el parametro que tiene los datos a actualizar (es un schema)
    db.commit()
    return {"message": post_query.first()}

    
