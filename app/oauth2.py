from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import classes, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

#auth.py -> @router.post("/login") -> tokenUrl="login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def criar_token_acesso(dado: dict):
    to_encode = dado.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verifica_token_acesso(token: str, credenciais_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # auth.py -> token_acesso = oauth2.criar_token_acesso(dado={"id_usuario":usuario_retornado.id}) -> payload.get("id_usuario")
        id: str = payload.get("id_usuario")
        if id is None:
            raise credenciais_exception
        token_data = classes.Token_data(id=id)
    except JWTError:
        raise credenciais_exception
    return token_data

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credenciais_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Não foi possível validar as credenciais", headers={"WWW-Authenticate":"Bearer"})
    token_verificado = verifica_token_acesso(token, credenciais_exception)
    usuario_retornado = db.query(models.Usuario).filter(models.Usuario.id == token_verificado.id).first()
    return usuario_retornado
