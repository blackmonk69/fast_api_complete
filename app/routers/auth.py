from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from .. import database,schemas,models


router=APIRouter(tags=['Authentication'])

@router.post ('/login')
def login(user_credentials:schemas.Class_UserLogin, db:session =Depends (database.get_db)):
   user= db.query(models.User).filter(models.User.email==user_credentials.email).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
       
     
