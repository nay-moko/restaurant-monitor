from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. استيراد الراوتات الموحدة من v1
from app.api.v1.router import api_router


app = FastAPI(
    title="Restaurant Floor Monitoring System",
    description="Backend API for real-time video monitoring and floor management",
    version="1.0.0",
)

# 2. إعدادات CORS (للسماح للفرونت إند بالاتصال)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. تضمين الراوتات الموحدة (Include Routers)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to Restaurant Monitoring API"}