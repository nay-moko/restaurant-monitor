# Main FastAPI Application Entry Point
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

app = FastAPI(
    title="Restaurant Floor Monitoring API",
    version="1.0.0"
)

@app.get("/health/db")
async def check_db_health(db: AsyncSession = Depends(get_db)):
    """اختبار صحة الاتصال بقاعدة البيانات"""
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "online", "db_response": result.scalar()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")