# نظام تطبيع أنواع المناطق (Zone Type Normalization)

## 🎯 الغرض
حل التعارض بين أنواع المناطق المستخدمة في API الجديد والقيم المتوقعة من AI Pipeline القديم.

## 🔄 التطبيع التلقائي

### الخريطة المطبقة:
- `customer_zone` → `table` (مناطق العملاء/الطاولات)
- `staff_zone` → `work` (مناطق الموظفين)
- `walkway` → `walk` (الممرات)
- `kitchen_area` → `work` (المطبخ)
- `entry_exit` → `walk` (المداخل والمخارج)

### التوافق مع الأنواع القديمة:
- `table_area` → `table`
- `staff_area` → `work`
- `service_path` → `walk`
- `hallway` → `walk`
- `corridor` → `walk`
- `entrance` → `walk`
- `buffet` → `work`
- `cashier` → `work`

## 📋 التطبيق

### في Schemas (`app/schemas/zone.py`):
1. خريطة `ZONE_TYPE_NORMALIZATION_MAP` - تعريف التطبيع
2. دالة `normalize_zone_type()` - تنفيذ التطبيع
3. `ZoneCreate.normalize_zone_type_field()` - تطبيع تلقائي عند الإنشاء
4. `ZoneUpdate.normalize_zone_type_field()` - تطبيع تلقائي عند التعديل

### في Endpoints (`app/api/v1/endpoints/zones.py`):
1. استيراد دالة التطبيع
2. تحديث التوثيق في Swagger UI
3. التعليقات في الكود تشير إلى التطبيع التلقائي

## ✅ النتيجة

### قبل الحل:
- الأدمن يدخل: `staff_zone`
- يُحفظ في قاعدة البيانات: `staff_zone` ❌
- AI Pipeline يقرأ: `staff_zone` ❌
- ZoneManager لا يجده في الخريطة: يكسر المنطق ❌

### بعد الحل:
- الأدمن يدخل: `staff_zone`
- يُطبع تلقائياً إلى: `work`
- يُحفظ في قاعدة البيانات: `work` ✅
- AI Pipeline يقرأ: `work` ✅
- ZoneManager يجده ويعمل بشكل صحيح ✅

## 🎯 المزايا

1. **لا تغيير في منطق AI** - ZoneManager يبقى كما هو
2. **قاعدة البيانات موحدة** - تحتوي فقط على القيم الصحيحة
3. **واجهة مرنة** - الأدمن يستخدم أسماء بديهية
4. **شفافية كاملة** - التطبيع تلقائي وموثق