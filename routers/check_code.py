from fastapi import APIRouter, Depends, HTTPException
from schemas.code import Code
from crud.code import check_code as check_code_crud
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post("/check_code", status_code=200)
async def check_code(code: Code,db: AsyncSession = Depends(get_db)):
    is_valid = await check_code_crud(code.value, db)
    if not is_valid:
        raise HTTPException(status_code=422, detail="Invalid code")
    return {"message": "Code is valid"}
