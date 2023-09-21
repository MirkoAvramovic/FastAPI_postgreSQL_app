"""
models.py - Database Models

This module defines the database models for the FastAPI application. These models are used to define the structure
of the database tables and the relationships between them.

Classes:
    - User: Represents a user in the application.
    - Item: Represents an item associated with a user.

"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    """
    User Model

    Represents a user in the application. This model defines the structure of the 'users' table in the database.

    Attributes:
        - id (int): The unique identifier for the user.
        - email (str): The email address of the user (unique).
        - hashed_password (str): The hashed password of the user.
        - is_active (bool): Indicates whether the user's account is active (default is True).

    Relationships:
        - items (relationship): A one-to-many relationship with the 'Item' model. Represents the items associated with the user.

    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    """
    Item Model

    Represents an item associated with a user. This model defines the structure of the 'items' table in the database.

    Attributes:
        - id (int): The unique identifier for the item.
        - title (str): The title of the item.
        - description (str): The description of the item.
        - owner_id (int): The foreign key referencing the 'id' of the user who owns the item.

    Relationships:
        - owner (relationship): A many-to-one relationship with the 'User' model. Represents the user who owns the item.

    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")