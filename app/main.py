from fastapi import FastAPI
from app.api.routes import auth
from app.db.mongodb import connect_to_mongo, close_mongo_connection

app = FastAPI(title="🚀 Advanced FastAPI + MongoDB")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB working!"}
