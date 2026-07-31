# تهيئة اتصال قاعدة البيانات (PostgreSQL / Async SQLAlchemy)
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# إنشاء المحرك الـ Async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # اجعلها True لو أردت طباعة استعلامات SQL في الـ Terminal
    future=True
)

# مصنع الجلسات الـ Async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base Class الموحد لجميع الـ Models
class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator:
    """Dependency لتمرير جلسة قاعدة البيانات للـ Endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()