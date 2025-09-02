from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel #pydantic para armar los schemas ( nos ayudan a trabajar con el body)
import uvicorn
from typing import Optional
from random import randrange
my_posts = [] #lo define como una lista

app= FastAPI()


    

def find_post(id):
    
    for p in my_posts: 
        if p['id'] == id:
            return p
   
    
#creamos una clase post con los attrib que deberia tener un post
class Class_Post (BaseModel):
    title:str
    content:str
    published:bool =True
    rating: Optional[int] = None
    

   
@app.get("/")  #este decorator lo convierte en una operation path de la api
def root(): # puede tener cualquier nombre, tratar que sea significativo
    return {"message":"Hello World2"}

@app.get("/posts")  #este decorator lo convierte en una operation path de la api
def get_posts(): # puede tener cualquier nombre, tratar que sea significativo
    return {"data":my_posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)   
 
def create_posts(Param_post : Class_Post): #este es formato Json
    #print (Param_post.title) #lo convierte de jason a lenguague comun
    #print (Param_post.content)
    #print (Param_post.model_dump()) #lo muestra como un diccionario 
    post_dicc=Param_post.model_dump() #el parametro que es json es convertido a dicc con el metodo model_dump
    post_dicc['id']=randrange(0,100000)  # le agrega la key id al post diccionario
    my_posts.append (post_dicc) #agrega un diccionario a la lista pero con una id
    
    return {"mensaje": post_dicc
            }

#ponerla al final para evitar que tome alguna anterior como valida
@app.get("/posts/{id}")
def buscar_post(id:int, param_response : Response):  #esto valida que sea un entero
    post=find_post(id)
    print (post)
    if not post:
        print ("no se encontro")
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"el id {id} no se encontro")
        # param_response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"el id {id} no se encontro"}
    return {"post detail": post}

#funcion que encuentra el index del id
def encuentra_index_id(id):
    for i, p in enumerate (my_posts):
        if p['id']==id:
            return i
            
    
    

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def borra_post(id:int, param_response : Response):     #esto valida que sea un entero
    index = encuentra_index_id(id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #retorna un status, no se puede retornar un mensaje json

@app.put("/post/{id}")
def actualiza_post(id:int, param_post: Class_Post):
    index = encuentra_index_id(id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    post_dicc=param_post.model_dump()
    post_dicc['id']=id #este agrega el campo id al diccionario, porque no lo trae de la clase Post
    my_posts[index]=post_dicc
    return {"message": post_dicc}

    
