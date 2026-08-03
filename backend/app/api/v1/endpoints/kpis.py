from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.core.security import get_current_admin
from app.models.customer_session import CustomerSession, CustomerSessionStatus

router = APIRouter()


@router.get("/realtime")
async def get_realtime_kpis(
    redis_client=Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    table_keys = await redis_client.keys("table:*:status")
    tables_occupied = 0
    tables_dirty = 0
    for key in table_keys:
        status = await redis_client.get(key)
        if status == "OCCUPIED":
            tables_occupied += 1
        elif status == "DIRTY":
            tables_dirty += 1

    worker_keys = await redis_client.keys("worker:*:status")
    workers_current = 0
    workers_active = 0
    workers_idle = 0
    worker_statuses = []  
    for key in worker_keys:
        entity_id = key.split(":", 2)[1]
        status = await redis_client.get(key)
        workers_current += 1
        if status == "ACTIVE":
            workers_active += 1
        elif status == "IDLE":
            workers_idle += 1
        worker_statuses.append({"entity_id": entity_id, "status": status})

    customers_result = await db.execute(
        select(func.count(CustomerSession.id)).where(
            CustomerSession.status == CustomerSessionStatus.ACTIVE
        )
    )
    customers_current = customers_result.scalar() or 0

    return {
        "tables_occupied": tables_occupied,
        "tables_dirty": tables_dirty,
        "customers_current": customers_current,
        "workers_current": workers_current,
        "workers_active": workers_active,
        "workers_idle": workers_idle,
        "worker_statuses": worker_statuses,
    }