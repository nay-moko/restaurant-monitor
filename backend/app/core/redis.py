# إدارة الاتصال بـ Redis (Pub/Sub & Fast State Store)
import redis.asyncio as aioredis
from app.core.config import settings

# جلب رابط Redis من الإعدادات أو استخدام الرابط الافتراضي
REDIS_URL = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")

# إنشاء كائن الاتصال المباشر بـ Redis
redis_client = aioredis.from_url(
    REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)