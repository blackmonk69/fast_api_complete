from .. import models,schemas,oauth
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 
from typing import List

router=APIRouter(prefix="/posts", tags=['Posts']) #este le dice que todos los routes comienzan con /post

#MUESTRA TODOS LOS POSTS
#--------------------------------------------------------------------------------------------------------
@router.get("/", response_model=List[schemas.Class_Response_Post])  #lee todos los posts
#en este caso es diferente el response porque aca devuelve TODOS los posts
def get_posts(db: Session = Depends(get_db)):
   print ("entro")
   posts=  db.query(models.Post).all() #le decimos un query de que model especifico, recordemos que los modelos son tablas
   return  posts

 #CREA UN POST
#--------------------------------------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED,
          response_model=schemas.Class_Response_Post)   #esto sirve para modelar la respuesta, la cual es nuevo_post pero con el formato del Response

def create_posts(posteo: schemas.Class_CreatePost , 
                 db: Session = Depends(get_db), user_id: int= Depends(oauth.get_current_user)): #no confundir uno es la clase post (schema) (que recibe los datos) y el otro el modelo post

    nuevo_post =  models.Post(**posteo.model_dump())
    db.add(nuevo_post) 
    db.commit()
    db.refresh(nuevo_post) 
    return nuevo_post

#TRAE UN POST
#-----------------------------------------------------------#-----------------------------------------------------------
#ponerla al final para evitar que tome alguna anterior como valida
@router.get("/{id}",  
         response_model=schemas.Class_Response_Post) #el response model va en el decorator, le dice q formato devolver en el return, NO el contenido,solo el formato

def buscar_post(id:int,     #esto valida que sea un entero
                db: Session = Depends(get_db)):  
    post_encontrado=db.query(models.Post).filter(models.Post.id==id).first()
    if not post_encontrado:
        print ("no se encontro")
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"el id {id} no se encontro")
    return post_encontrado

#BORRA UN POST
#-----------------------------------------------------------#-----------------------------------------------------------
@router.delete("/{id}") #BORRRA UN POST
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
@router.put("/{id}",
        response_model=schemas.Class_Response_Post)
def actualiza_post(id:int, param_post: schemas.Class_CreatePost,db: Session = Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    post_encontrado=post_query.first()
    if post_encontrado is None:
        raise HTTPException(status_code=404, detail=f"Post {id} no encontrado")
    post_query.update(param_post.model_dump(),synchronize_session=False)#se le pasa el parametro que tiene los datos a actualizar (es un schema)
    db.commit()
    return  post_query.first()