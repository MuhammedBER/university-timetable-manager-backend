from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password : str)->str:
    password_bytes = password.encode('utf-8')
    safe_bytes = password_bytes[:72]
    hashed = bcrypt.hashpw(safe_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain : str, hashed:str):
    password_bytes = plain.encode('utf-8')[:72]
    return bcrypt.checkpw(password_bytes, hashed.encode('utf-8'))