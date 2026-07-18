from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud.config import query_locale

router = APIRouter(prefix="/config")

@router.get("/locale", status_code=200)
async def get_locale(db: AsyncSession = Depends(get_db)):
    try:
        locale = await query_locale(db)
    except ValueError:
        raise HTTPException(422, "No locale file")
    return locale