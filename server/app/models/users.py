from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class User(BaseModel):
    email: EmailStr = Field(unique=True)
    name: str
    password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
