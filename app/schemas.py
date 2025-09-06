from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

#----------------------------------------------------------------------------------
#ESTO ES UN SCHEMA, SIRVE PARA MODELAR EL REQUEST, TAMBIEN SE PUEDE DEFINIR UN SCHEMA PARA MODELAR EL RESPONSE

class Class_Post_Base(BaseModel): #creamos una clase post con los attrib que deberia tener un post
    title:str              #esto es un schema
    content:str
    published:bool =True 

class Class_CreatePost(Class_Post_Base): #extiende la clase base
     pass   
        

class Class_Response_Post(Class_Post_Base): #hereda de la clase post base y agrega dos campos mas
    id:int
    created_at: datetime
    class Config:
        from_attributes = True #cuando es un response, una salida, se coloca esta config
        
class Class_UserCreate(BaseModel):
    email:EmailStr
    password:str    

class Class_UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True  #cuando es un response, una salida, se coloca esta config
        
class Class_UserLogin(BaseModel):
    email:EmailStr
    password: str 
    class Config:
        from_attributes = True  #cuando es un response, una salida, se coloca esta config  

class Class_Token(BaseModel):
    access_token:str
    token_type:str
    
class Class_Token_Data(BaseModel):
    id:Optional [int]=None                  