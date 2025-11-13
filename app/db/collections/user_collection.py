from app.db.mongodb import mongodb
from app.models.user import UserModel

async def create_user(user_data: dict):
    result = await mongodb.db["users"].insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    return await mongodb.db["users"].find_one({"email": email})
