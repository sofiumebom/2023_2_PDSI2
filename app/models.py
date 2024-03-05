from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True, nullable=False)
    titulo = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    publicada = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Usuario")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Voto(Base):
    __tablename__ = "votos"
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    mensagem_id = Column(Integer, ForeignKey("mensagens.id", ondelete="CASCADE"), primary_key=True)
