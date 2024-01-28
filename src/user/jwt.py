import jwt

from datetime import datetime, timedelta

SECRET_KEY = 'my_secret_key'
ALGORITHM = 'HS256'
EXPIRATION_TIME = timedelta(hours=2)


def create_jwt(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({'exp': expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token: str):
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_data
    except jwt.PyJWTError:
        return None
