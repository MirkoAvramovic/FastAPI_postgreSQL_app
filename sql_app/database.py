"""
database.py

This module handles the database configuration and session management using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the URL to your PostgreSQL database. You can switch between databases by
# modifying the value of SQLALCHEMY_DATABASE_URL.
# For SQLite, use "sqlite:///./sql_app.db" as the database URL.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Admin@localhost:5432/employee_database"

# Create a SQLAlchemy engine that will connect to the specified database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory (sessionmaker) for managing database sessions.
# The sessions will be used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative models.
# This base class will be used for defining your database models (tables).
Base = declarative_base()