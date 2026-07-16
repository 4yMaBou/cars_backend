from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud.auth import check_credentials
from schemas.auth import Auth
from auth.jwt import create_token

router = APIRouter(prefix="/auth")

@router.post("/login", status_code=200)
async def login(auth: Auth, db: AsyncSession = Depends(get_db)):
    credentials = await check_credentials(auth.username, auth.password, db)
    if not credentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(auth.username)
    return {"access_token": token, "token_type": "bearer"}