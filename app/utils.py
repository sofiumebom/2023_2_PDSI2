from passlib.context import CryptContext

senha_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_senha(senha: str):
    return senha_context.hash(senha)

def verifca_senha(senha_digitada, senha_hashed):
    return senha_context.verify(senha_digitada, senha_hashed)