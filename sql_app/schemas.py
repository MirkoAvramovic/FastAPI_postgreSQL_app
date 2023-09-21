from pydantic import BaseModel, EmailStr
from typing import Optional

class ItemBase(BaseModel):
    """
    Schema for creating or updating an item.
    """
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    """
    Schema for creating a new item.
    """
    pass

class Item(ItemBase):
    """
    Schema for retrieving an item.
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    email: EmailStr  # Use EmailStr for email validation

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

class User(UserBase):
    """
    Schema for retrieving a user's data.
    """
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    """
    Schema for updating user data.
    Include fields you want to allow for update.
    """
    email: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
