

from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session



#hay que pasarle 3 cosas
#SECRET_KEY
#INDICAR QUE ALGORITMO SE VA A USAR
#TIEMPO DE EXPIRACION DEL TOKEN

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "mi_super_clave"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme=OAuth2PasswordBearer (tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()   # siempre dict
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    token = token.strip()
    print("Token recibido:", repr(token))  # revisá cómo llega
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print (payload)
        id: int = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.Class_Token_Data(id=id)
        return token_data
    except JWTError as e:
        print ("JWTError detectado:", e)
        raise credentials_exception
    

    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first() #

    return user