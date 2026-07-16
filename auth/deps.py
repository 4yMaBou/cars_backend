from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import decode_token
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from crud.auth import get_user



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def check_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> None:
    try:
        payload = decode_token(token)
        username = payload["username"]
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        user = await get_user(username, db)
        if exp < datetime.now(timezone.utc) - timedelta(hours=24) or user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    return None