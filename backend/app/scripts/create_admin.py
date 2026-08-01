from app.core.database import AsyncSessionLocal  # 👈 التعديل هنا
from app.core.security import hash_password
from app.models.admin import Admin
from app.core.config import settings
import asyncio
from sqlalchemy.future import select

async def create_admin():
    async with AsyncSessionLocal() as db:  # 👈 واستخدامه هنا
        try:
            email = settings.INITIAL_ADMIN_EMAIL
            password = settings.INITIAL_ADMIN_PASSWORD

            stmt = select(Admin).where(Admin.email == email)
            result = await db.execute(stmt)
            existing_admin = result.scalars().first()

            if existing_admin:
                print("Admin already exists.")
                return

            admin = Admin(
                email=email,
                password_hash=hash_password(password),
            )

            db.add(admin)
            await db.commit()

            print("Admin created successfully.")

        except Exception as e:
            await db.rollback()
            print(f"Error creating admin: {e}")

if __name__ == "__main__":
    asyncio.run(create_admin())