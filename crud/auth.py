from models.setting import Setting
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from enum import IntFlag, auto

class CredentialsStatus(IntFlag):
    NONE = 0

    EXISTS = auto()
    VALID = auto()

    OK = EXISTS | VALID

async def check_credentials(login: str, password: str, db: AsyncSession) -> bool:
    status = CredentialsStatus.NONE
    query = select(Setting).where(Setting.key == "credentials" and Setting.value["username"] == login)
    credentials = await db.execute(query)
    _credentials = credentials.scalar_one_or_none()
    
    status |= CredentialsStatus.EXISTS * (_credentials is not None)
    status |= CredentialsStatus.VALID * bool(_credentials and bcrypt.checkpw(password.encode('utf-8'), _credentials.value["password"].encode('utf-8'))) #избыточно, посути одним условием все проверям
    
    return bool(status == CredentialsStatus.OK)

async def get_user(username: str, db: AsyncSession) -> bool:
    query = select(Setting).where(Setting.key == "credentials" and Setting.value["username"] == username)
    credentials = await db.execute(query)
    credentials = credentials.scalar_one_or_none()
    return credentials is not None