from .. import models, classes, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/voto", tags=['Voto'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def votar(novo_voto: classes.Voto, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.get_usuario_atual)):
    mensagem_encontrada = db.query(models.Mensagem).filter(models.Mensagem.id == novo_voto.mensagem_id).first()
    if not mensagem_encontrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensagem com id: {novo_voto.mensagem_id} não existe")

    voto_query = db.query(models.Voto).filter(models.Voto.mensagem_id == novo_voto.mensagem_id, models.Voto.usuario_id == usuario_atual.id)

    voto_encontrado = voto_query.first()
    if(novo_voto.dir == 1):
        if voto_encontrado:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Usuário {usuario_atual.id} já votou na mensagem {novo_voto.mensagem_id}")
        else:
            voto_salvar = models.Voto(mensagem_id = novo_voto.mensagem_id, usuario_id = usuario_atual.id)
        db.add(voto_salvar)
        db.commit()
        return {"Retorno":"Voto adicionado com Sucesso"}
    else:
        if not voto_encontrado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voto não existe")
        else:
            voto_query.delete(synchronize_session=False)
            db.commit()
            return {"Retorno":"Voto deletado com Sucesso"}

