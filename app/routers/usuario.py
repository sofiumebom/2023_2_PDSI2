from .. import models, classes, utils
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=['usuarios'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=classes.Usuario_Retornado)
def criar_usuario(novo_usuario: classes.Usuario_Criar, db: Session = Depends(get_db)):
    hash_senha = utils.hash_senha(novo_usuario.senha)
    novo_usuario.senha = hash_senha
    usuario_criado = models.Usuario(**novo_usuario.model_dump())
    db.add(usuario_criado)
    db.commit()
    db.refresh(usuario_criado)
    return usuario_criado

@router.get("/{id}", response_model=classes.Usuario_Retornado)
def get_msg(id: int, db: Session = Depends(get_db)):
    usuario_encontrado = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if usuario_encontrado == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com o id {id} não foi encontrado")
    return usuario_encontrado