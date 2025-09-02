from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel #pydantic para armar los schemas ( nos ayudan a trabajar con el body)
import uvicorn
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
             
   

class Class_Post (BaseModel): #creamos una clase post con los attrib que deberia tener un post
    title:str              
    content:str
    published:bool =True
     

   
@app.get("/")  #este decorator lo convierte en una operation path de la api
def root(): # puede tener cualquier nombre, tratar que sea significativo
    return {"message":"Hello World2"}

@app.get("/posts")  #lee todos los posts
def get_posts():
    cursor.execute("""select * from posts""") 
    posts=cursor.fetchall()
    return {"data":posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)   
 
def create_posts(Param_post : Class_Post): #este es formato Json
    cursor.execute("""insert into posts (title, content, published) values (%s,%s,%s) RETURNING *""", 
                   (Param_post.title, Param_post.content, Param_post.published))
    nuevo_post=cursor.fetchone()
    conn.commit()
    return {"mensaje": nuevo_post}

           

#ponerla al final para evitar que tome alguna anterior como valida
@app.get("/posts/{id}")
def buscar_post(id:int):  #esto valida que sea un entero
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post_encontrado = cursor.fetchone()
    if not post_encontrado:
        print ("no se encontro")
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"el id {id} no se encontro")
 
    return {"post detail": post_encontrado}


@app.delete("/posts/{id}") #BORRRA UN POST
def borra_post(id:int):     #esto valida que sea un entero
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    post_borrado=cursor.fetchone()
    #print (post_borrado)
    if post_borrado is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    conn.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def actualiza_post(id:int, param_post: Class_Post):
    cursor.execute ("update posts set title=%s,content=%s,published=%s where id=%s returning *",
                    (param_post.title,param_post.content,param_post.published, id))
    post_actualizado=cursor.fetchone()
    conn.commit()
    if post_actualizado is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    
    return {"message": post_actualizado}

    
