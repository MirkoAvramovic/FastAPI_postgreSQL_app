"""
CRUD Operations for User and Item Data

This module provides functions to perform CRUD (Create, Read, Update, Delete)
operations on User and Item data using SQLAlchemy and FastAPI.

Functions:
    - get_user(db: Session, user_id: int) -> models.User:
        Retrieve a User by their ID.
        
    - get_user_by_email(db: Session, email: str) -> models.User:
        Retrieve a User by their email address.
        
    - get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        Retrieve a list of Users with optional pagination.
        
    - create_user(db: Session, user: schemas.UserCreate) -> models.User:
        Create a new User with the provided data.
        
    - get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
        Retrieve a list of Items with optional pagination.
        
    - create_user_item(db: Session, item: schemas.ItemCreate, user_id: int) -> models.Item:
        Create a new Item associated with a User.
        
    - update_user(db: Session, user_id: int, updated_user: schemas.UserUpdate) -> models.User:
        Update User data with the provided changes.
        
    - delete_user(db: Session, user_id: int) -> Union[models.User, schemas.User]:
        Delete a User by their ID and return the deleted User.

Note:
    - This module interacts with the database using SQLAlchemy ORM.
    - It uses models and schemas defined in other modules for data handling.
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

# Create an instance of the password hashing library
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_user(db: Session, user_id: int, updated_user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in updated_user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user or schemas.User()  # Return an empty User instance if db_user is None