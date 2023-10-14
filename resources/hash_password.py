from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=['pbkdf2_sha256'],
    default='pbkdf2_sha256')

def hash_password(senha):
    return pwd_context.hash(senha)


def check_hashed_password(senha, hashed):
    return pwd_context.verify(senha,hashed)