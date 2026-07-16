import jwt
import datetime
from auth.keys import read_keys

def create_token(username: str) -> str:
    private_key, public_key = read_keys()
    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, private_key, algorithm="EdDSA")    
    return token

def decode_token(token: str) -> []:
    private_key, public_key = read_keys()
    payload = jwt.decode(token, public_key, algorithms=["EdDSA"])
    return payload