from .. import models, classes, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(prefix="/mensagens", tags=['mensagens'])

@router.get("/", response_model=List[classes.Mensagem_Retornada_Voto])
def teste(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual), Limite: int = 10, Pular: int = 0, Search: Optional[str]=""):
    mensagens_votos = db.query(models.Mensagem, func.count(models.Voto.mensagem_id).label("votos")).join(models.Voto, models.Voto.mensagem_id == models.Mensagem.id, isouter=True).group_by(models.Mensagem.id).filter(models.Mensagem.titulo.contains(Search)).limit(Limite).offset(Pular).all()

    mensagens_votos = list (map (lambda x : x._mapping, mensagens_votos))

    return mensagens_votos

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=classes.Mensagem_Retornada)
def criar_valores(nova_mensagem: classes.Mensagem_Criar, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual)):
    mensagem_criada = models.Mensagem(owner_id = usuario_atual.id, **nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    print(mensagem_criada)
    return mensagem_criada

@router.get("/{id}", response_model=classes.Mensagem_Retornada_Voto)
def get_msg(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual)):
    mensagem_encontrada = db.query(models.Mensagem, func.count(models.Voto.mensagem_id).label("votos")).join(models.Voto, models.Voto.mensagem_id == models.Mensagem.id, isouter=True).group_by(models.Mensagem.id).filter(models.Mensagem.id == id).first()
    if not mensagem_encontrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensagem com o id {id} não foi encontrada")
    return mensagem_encontrada

@router.delete("/{id}", response_model=List[classes.Mensagem_Retornada])
def delete_msg(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual)):
    todas_mensagens = None
    encontrar_mensagem_query = db.query(models.Mensagem).filter(models.Mensagem.id == id)
    if encontrar_mensagem_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensagem com o id {id} não foi encontrada")
    elif encontrar_mensagem_query.first().owner_id != usuario_atual.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Você não está autorizado para realizar esta requisição")
    else:
        encontrar_mensagem_query.delete(synchronize_session=False)
        db.commit()
        todas_mensagens = db.query(models.Mensagem).all()
    return todas_mensagens

@router.put("/{id}", response_model=List[classes.Mensagem_Retornada])
def update_msg(id: int, mensagem_atualizada: classes.Mensagem_Criar, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual)):
    encontrar_mensagem_query = db.query(models.Mensagem).filter(models.Mensagem.id == id)
    if encontrar_mensagem_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensagem com o id {id} não foi encontrada")
    elif encontrar_mensagem_query.first().owner_id != usuario_atual.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Você não está autorizado para realizar esta requisição")
    else:
        encontrar_mensagem_query.update(mensagem_atualizada.model_dump(), synchronize_session=False)
        db.commit()
        todas_mensagens = db.query(models.Mensagem).all()
    return todas_mensagens
