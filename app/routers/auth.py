from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from .. import database,schemas,models,utils,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(tags=['Authentication'])

@router.post ('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:session =Depends (database.get_db)):
   user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
  
   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"usuario no encontrado nvalid Credentials")
       
   if not utils.verify (user_credentials.password,user.password):
       raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail=f"verificacion fallida invalid credentials")
   
   #create token
   #return token
   
   access_token = oauth.create_access_token(data={"user_id": user.id})
   print ("entrooo",user)
   return {"access token":access_token, "token_type":"bearer"}
     
