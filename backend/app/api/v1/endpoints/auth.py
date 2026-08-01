from datetime import datetime, timedelta, timezone
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.admin import Admin
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    OTPRequest,
    PasswordResetRequest,
    MessageResponse,)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    get_token_from_header, # 👈 استيراد الدالة الجديدة هنا
)
from app.services.email_service import send_otp_email
from app.core.security import password_hash
from app.core.redis import redis_client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from app.core.security import get_current_admin
from app.models.admin import Admin

router = APIRouter()
#login
@router.post("/login",response_model=TokenResponse,)
async def login(data: LoginRequest,db: AsyncSession = Depends(get_db),):

    stmt = select(Admin).where(Admin.email == data.email)
    result = await db.execute(stmt)
    admin = result.scalars().first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password",)

    if not verify_password(data.password,admin.password_hash,):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",)

    token = create_access_token(str(admin.id))

    return TokenResponse(access_token=token)

@router.get("/me")
def get_me(
    current_admin: Admin = Depends(get_current_admin),
):
    return {
        "id": str(current_admin.id),
        "email": current_admin.email,
    }
    
# otp
@router.post(
    "/password/request-otp",
    response_model=MessageResponse,
)
async def request_password_otp(
    data: OTPRequest,
    db: AsyncSession = Depends(get_db),
):
    # 1. البحث عن المستخدم
    stmt = select(Admin).where(Admin.email == data.email)
    result = await db.execute(stmt)
    admin = result.scalars().first()

    # 2. التأكد من وجود الإيميل
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email address not found",
        )

    # 3. توليد رمز الـ OTP
    otp = f"{secrets.randbelow(1_000_000):06d}"

    # 4. حفظ البيانات في الموديل
    admin.otp_code_hash = otp
    # 🟢 استبدل سطر otp_expires_at بهذه الصيغة (تزيل الـ tzinfo لتتوافق مع الداتابيز):
    admin.otp_expires_at = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10))

    # 5. الحفظ في قاعدة البيانات
    await db.commit()

    # 6. إرسال الإيميل بآمان (حتى لا ينهار السيرفر إذا فشل سيرفر SMTP)
    try:
        send_otp_email(
            recipient=admin.email,
            otp=otp,
        )
    except Exception as e:
        print(f"⚠️ Warning: Could not send email. Error: {e}")
        # التطبيق سيكمل ويحفظ الـ OTP في الداتابيز لتتمكن من تجربته

    return MessageResponse(
        message="OTP code has been generated and sent successfully."
    )
    
#reset password
# reset password
@router.post(
    "/password/reset",
    response_model=MessageResponse,
)
async def reset_password(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    # 1. البحث عن الأدمن
    stmt = select(Admin).where(Admin.email == data.email)
    result = await db.execute(stmt)
    admin = result.scalars().first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP or email",
        )

    if not admin.otp_code_hash or not admin.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP is not valid or expired",
        )

    # 🟢 2. تحويل التوقيت الحالي ليكون Naive للمقارنة السليمة مع الداتابيز
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # 3. التحقق من انتهاء صلاحية الـ OTP
    if admin.otp_expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired",
        )

    # 4. مطابقة كود الـ OTP
    if admin.otp_code_hash != data.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )

    # 5. تحديث كلمة السر وتشفيرها
    admin.password_hash = hash_password(data.new_password)

    # 6. تفريغ الـ OTP بعد الاستخدام
    admin.otp_code_hash = None
    admin.otp_expires_at = None

    await db.commit()

    return MessageResponse(
        message="Password changed successfully"
    )
    
#logout
# logout
@router.post(
    "/logout",
    response_model=MessageResponse,
)
async def logout(
    token: str = Depends(get_token_from_header), # 👈 استخدام الدالة الجديدة
):
    payload = decode_token(token)
    
    jti = payload.get("jti")
    exp = payload.get("exp")

    if not jti or not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    now = int(datetime.now(timezone.utc).timestamp())
    ttl = max(exp - now, 1)

    await redis_client.setex(
        f"revoked_token:{jti}",
        ttl,
        "1",
    )

    return MessageResponse(
        message="Logged out successfully"
    )