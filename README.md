# FastAPI PostgreSQL App

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.4-blue)

This is a sample FastAPI application with a PostgreSQL database backend. It demonstrates how to create a RESTful API using FastAPI and interact with a PostgreSQL database to manage users and items.

## Features

- Create, read, update, and delete users and items via API endpoints.
- Hashed passwords for users
- PostgreSQL database integration using SQLAlchemy.
- Pydantic models for data validation and serialization.
- Interactive API documentation with Swagger UI (available at `/docs`).

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 13.4 or higher

## Getting Started

Clone this repository:

   ```bash
   git clone https://github.com/yourusername/FastAPI_postgreSQL_app.git

Change to the project directory:
cd FastAPI_postgreSQL_app

Install project dependencies:
pip install -r requirements.txt

Configure the database connection in sql_app/database.py:
SQLALCHEMY_DATABASE_URL = "postgresql://yourusername:yourpassword@localhost:5432/employee_database"

Apply database migrations:
alembic upgrade head

Start the FastAPI application:
uvicorn sql_app.main:app --reload

Access the interactive API documentation at http://127.0.0.1:8000/docs.
