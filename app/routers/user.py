from .. import models,schemas,utils
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 

router=APIRouter(prefix="/users", tags=['Users'])

#crea un usuario
#----------------------------------------------------------------------------
@router.post("/",
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.Class_UserOut)   #esto sirve para modelar la respuesta, la cual es nuevo_post pero con el formato del Response

def create_user(user: schemas.Class_UserCreate , 
                 db: Session = Depends(get_db)): #no confundir uno es la clase post (schema) (que recibe los datos) y el otro el modelo post
   
    #hash the password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    nuevo_user =  models.User(**user.model_dump())
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    return nuevo_user


@router.get ('/{id}', response_model=schemas.Class_UserOut)
def get_user(id:int,
             db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
   
    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    
    return user
   