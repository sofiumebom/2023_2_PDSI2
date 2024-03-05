# uvicorn aula:app --reload

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import mensagem, usuario, auth, voto

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(mensagem.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(voto.router)

@app.get("/")
def read_root():
    return {"Hello": "lala"}