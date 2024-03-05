
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class Mensagem_Base(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True
    # rating: Optional[int] = None

class Mensagem_Criar(Mensagem_Base):
    #pass = "não faça nada"
    pass

class Usuario_Retornado(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class Mensagem_Retornada(Mensagem_Base):
    id: int
    created_at: datetime
    owner_id: int
    owner: Usuario_Retornado
    class Config:
        from_attributes = True

class Mensagem_Retornada_Voto(BaseModel):
    Mensagem: Mensagem_Retornada
    votos: int
    class Config:
        from_attributes = True

class Usuario_Criar(BaseModel):
    email: EmailStr
    senha: str

class Usuario_Login(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    token_acesso: str
    token_tipo: str

class Token_data(BaseModel):
    id: Optional[int] = None

class Voto(BaseModel):
    mensagem_id: int
    # ge = Greater or Equal
    # le = Less or Equal
    dir: conint(ge=0, le=1)




