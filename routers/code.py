from fastapi import APIRouter, Depends, HTTPException
from schemas.code import Code
from crud.code import check_code as check_code_crud, list_codes as list_codes_crud, create_code as create_code_crud
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter(prefix="/code")

@router.get("/list")
async def list_codes(db: AsyncSession = Depends(get_db)) -> list[Code]:
    codes = await list_codes_crud(db)
    return codes

@router.post("/check", status_code=200)
async def check_code(code: Code,db: AsyncSession = Depends(get_db)):
    is_valid = await check_code_crud(code.uuid, db)
    if not is_valid:
        raise HTTPException(status_code=422, detail="Invalid code")
    return {"message": "Code is valid"}

@router.post("/create", status_code=200)
async def create_code(db: AsyncSession = Depends(get_db)):
    try:
        code = await create_code_crud(db)
        return {"message": "Code created successfully", "code": code.uuid}
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=422, detail="Failed to create code")

@router.post("/delete", status_code=200)
async def delete_codes(timestamp: datetime, db: AsyncSession = Depends(get_db)):
    try:
        await delete_codes_crud(timestamp, db)
        return {"message": "Codes deleted successfully"}
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=422, detail="Failed to delete codes")