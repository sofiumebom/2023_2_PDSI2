from .. import models, classes, utils, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Autenticação'])

@router.post("/login", response_model=classes.Token)
def login(usuario_credenciais: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_retornado = db.query(models.Usuario).filter(models.Usuario.email==usuario_credenciais.username).first()
    if not usuario_retornado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Informações Inválidas")
    elif not utils.verifca_senha(usuario_credenciais.password, usuario_retornado.senha):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Informações Inválidas")
    else:
        token_acesso = oauth2.criar_token_acesso(dado={"id_usuario": usuario_retornado.id})
        return {"token_acesso": token_acesso, "token_tipo": "bearer"}
