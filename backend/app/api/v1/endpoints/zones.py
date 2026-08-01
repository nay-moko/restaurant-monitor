# إدارة المضلعات (Zones)، الصور اللحظية (Snapshots)
from pathlib import Path
from fastapi.responses import FileResponse
from typing import List
from uuid import uuid4
import io
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.admin import Admin
from app.models.camera import Camera
from app.models.zone import Zone
from app.schemas.zone import (
    ZoneCreate,
    ZoneUpdate,
    ZoneResponse,
    ZoneListResponse,
    PolygonCoordinates
)

router = APIRouter()


# 📌 البحث الديناميكي عن المجلد الرئيسي الذي يحتوي على مجلد data
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = None

for parent in CURRENT_FILE.parents:
    if (parent / "data").exists():
        PROJECT_ROOT = parent
        break

# إذا لم يجده، نحدد المسار الافتراضي للـ data
if PROJECT_ROOT:
    REF_FRAMES_DIR = PROJECT_ROOT / "data" / "debug" / "zones" / "reference_frames"
else:
    # مسار احتياطي مباشر
    REF_FRAMES_DIR = Path("C:/Users/hp/Desktop/restaurant-monitor/data/debug/zones/reference_frames")


@router.get(
    "/cameras/{camera_id}/snapshot",
    summary="Get Camera Snapshot",
    description="Returns the reference image for the specified camera."
)
async def get_camera_snapshot(
    camera_id: str,
    current_admin: Admin = Depends(get_current_admin)
):
    # 1. البحث عن الصورة المرجعية لخلفية الرسم
    ref_image_jpg = REF_FRAMES_DIR / f"{camera_id}_reference.jpg"
    ref_image_png = REF_FRAMES_DIR / f"{camera_id}_reference.png"

    # طباعة المسار في الـ Terminal للتأكد من المكان الذي يبحث فيه
    print(f"📸 Checking for snapshot at: {ref_image_jpg}")

    if ref_image_jpg.exists():
        return FileResponse(path=ref_image_jpg, media_type="image/jpeg")
    elif ref_image_png.exists():
        return FileResponse(path=ref_image_png, media_type="image/png")

    # 2. في حال عدم وجود صورة لهذا الاسم تحديدا
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Image not found for '{camera_id}'. Looked at: {ref_image_jpg}"
    )

@router.get(
    "/cameras/{camera_id}",
    response_model=List[ZoneResponse],
    summary="استعراض مناطق كاميرا معينة",
    description="""
    يسترجع جميع المناطق المحددة لكاميرا معينة.
    
    يمكن استخدام هذه المناطق لعرضها على خريطة الكاميرا في الواجهة الأمامية.
    """,
    responses={
        200: {"description": "تم استرجاع المناطق بنجاح"},
        404: {"description": "الكاميرا غير موجودة"}
    }
)
async def get_zones_by_camera(
    camera_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    استعراض جميع المناطق المحددة لكاميرا معينة.
    """
    # 1. التحقق من وجود الكاميرا
    stmt = select(Camera).where(Camera.id == camera_id)
    result = await db.execute(stmt)
    camera = result.scalars().first()
    
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"الكاميرا ذات المعرف {camera_id} غير موجودة"
        )
    
    # 2. استرجاع المناطق المرتبطة بالكاميرا
    stmt = select(Zone).where(Zone.camera_id == camera_id)
    result = await db.execute(stmt)
    zones = result.scalars().all()
    
    return zones


@router.post(
    "/",
    response_model=ZoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="إضافة منطقة جديدة",
    description="""
    إضافة منطقة اهتمام جديدة للكاميرا المحددة.
    
    يجب توفير:
    - camera_id: معرف الكاميرا
    - name: اسم المنطقة
    - zone_type: نوع المنطقة (customer_zone, staff_zone, walkway, table_area, etc.)
    - polygon_coordinates: إحداثيات المضلع
    
    الحقول الاختيارية:
    - parent_zone_id: معرف المنطقة الأب
    - excludes_tables: استثناء الطاولات
    - auto_generated: إنشاء تلقائي
    """,
    responses={
        201: {"description": "تم إنشاء المنطقة بنجاح"},
        400: {"description": "بيانات غير صالحة"},
        404: {"description": "الكاميرا غير موجودة"}
    }
)
async def create_zone(
    zone_data: ZoneCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    إضافة منطقة اهتمام جديدة.
    """
    # 1. التحقق من وجود الكاميرا
    stmt = select(Camera).where(Camera.id == zone_data.camera_id)
    result = await db.execute(stmt)
    camera = result.scalars().first()
    
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"الكاميرا ذات المعرف {zone_data.camera_id} غير موجودة"
        )
    
    # 2. التحقق من parent_zone_id إذا تم توفيره
    if zone_data.parent_zone_id:
        stmt = select(Zone).where(Zone.id == zone_data.parent_zone_id)
        result = await db.execute(stmt)
        parent_zone = result.scalars().first()
        
        if not parent_zone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المنطقة الأب ذات المعرف {zone_data.parent_zone_id} غير موجودة"
            )
    
    # 3. إنشاء المنطقة الجديدة
    zone_id = str(uuid4())
    new_zone = Zone(
        id=zone_id,
        camera_id=zone_data.camera_id,
        parent_zone_id=zone_data.parent_zone_id,
        name=zone_data.name,
        zone_type=zone_data.zone_type,
        polygon_coordinates=zone_data.polygon_coordinates.to_dict(),
        auto_generated=zone_data.auto_generated,
        excludes_tables=zone_data.excludes_tables
    )
    
    db.add(new_zone)
    await db.commit()
    await db.refresh(new_zone)
    
    return new_zone


@router.put(
    "/{zone_id}",
    response_model=ZoneResponse,
    summary="تعديل منطقة موجودة",
    description="""
    تعديل بيانات منطقة موجودة (اسم، نوع، إحداثيات، إلخ).
    
    جميع الحقول اختيارية، مما يسمح بالتعديل الجزئي.
    فقط الحقول المرسلة سيتم تحديثها.
    """,
    responses={
        200: {"description": "تم تحديث المنطقة بنجاح"},
        400: {"description": "بيانات غير صالحة"},
        404: {"description": "المنطقة غير موجودة"}
    }
)
async def update_zone(
    zone_id: str,
    zone_data: ZoneUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    تعديل منطقة موجودة.
    """
    # 1. التحقق من وجود المنطقة
    stmt = select(Zone).where(Zone.id == zone_id)
    result = await db.execute(stmt)
    zone = result.scalars().first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"المنطقة ذات المعرف {zone_id} غير موجودة"
        )
    
    # 2. تحديث الحقول المرسلة فقط
    update_data = zone_data.model_dump(exclude_unset=True)
    
    # 👈 التصحيح: الوصول للشيء الأصلي من zone_data قبل تحويله لـ dict
    if zone_data.polygon_coordinates is not None:
        update_data['polygon_coordinates'] = zone_data.polygon_coordinates.to_dict()
    
    # 3. التحقق من parent_zone_id إذا تم تعديله
    if zone_data.parent_zone_id is not None:
        stmt = select(Zone).where(Zone.id == zone_data.parent_zone_id)
        result = await db.execute(stmt)
        parent_zone = result.scalars().first()
        
        if not parent_zone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المنطقة الأب ذات المعرف {zone_data.parent_zone_id} غير موجودة"
            )
            
    # 4. تطبيق التعديلات على كائن الداتابيز
    for field, value in update_data.items():
        setattr(zone, field, value)
    
    await db.commit()
    await db.refresh(zone)
    
    return zone

@router.delete(
    "/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="حذف منطقة",
    description="""
    حذف منطقة محددة بناءً على معرفها.
    
    **تنبيه:** حذف المنطقة سيؤدي إلى حذف جميع المناطق الفرعية المرتبطة بها
    بسبب استخدام CASCADE في قاعدة البيانات.
    """,
    responses={
        204: {"description": "تم حذف المنطقة بنجاح"},
        404: {"description": "المنطقة غير موجودة"}
    }
)
async def delete_zone(
    zone_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    حذف منطقة محددة.
    """
    # 1. التحقق من وجود المنطقة
    stmt = select(Zone).where(Zone.id == zone_id)
    result = await db.execute(stmt)
    zone = result.scalars().first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"المنطقة ذات المعرف {zone_id} غير موجودة"
        )
    
    # 2. حذف المنطقة
    await db.delete(zone)
    await db.commit()
    
    return None