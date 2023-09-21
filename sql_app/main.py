from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from passlib.context import CryptContext
from .database import SessionLocal, engine

#Create an instance of the FastAPI application
app = FastAPI()

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Dependency function to get a database session
def get_db():
    """
    Dependency function to get a database session.
    
    Returns:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a CryptContext instance with a secret key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Endpoint to create a new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Endpoint to retrieve a list of users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of users.

    Args:
        skip (int): Number of users to skip.
        limit (int): Maximum number of users to return.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[schemas.User]: A list of user data.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Read a User by ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their unique ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        User: The user's details.
    
    Raises:
        HTTPException:
            - 404 (Not Found): If the user with the specified ID was not found.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Read a User by Email
@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user.

    Returns:
        User: The user's details.
    
    Raises:
        HTTPException:
            - 404 (Not Found): If the user with the specified email address was not found.
    """
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create an Item for a User
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Create an item for a specific user based on their unique ID.

    Args:
        user_id (int): The unique identifier of the user for whom the item is created.
        item (ItemCreate): The item details to create for the user.

    Returns:
        Item: The created item's details.
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# Read Items (with Pagination)
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of items with optional pagination.

    Args:
        skip (int, optional): The number of items to skip (for pagination).
        limit (int, optional): The maximum number of items to include in the response (for pagination).

    Returns:
        List[Item]: List of items based on the specified pagination settings.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# Update a User
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's information based on their unique ID.

    Args:
        user_id (int): The unique identifier of the user to update.
        updated_user (UserUpdate): The user details to update.

    Returns:
        User: The updated user's details.
    
    Raises:
        HTTPException:
            - 404 (Not Found): If the user with the specified ID was not found.
    """
    db_user = crud.update_user(db, user_id, updated_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete a User
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user based on their unique ID.

    Args:
        user_id (int): The unique identifier of the user to delete.

    Returns:
        Dict: A message confirming the deletion.
    
    Raises:
        HTTPException:
            - 404 (Not Found): If the user with the specified ID was not found.
    """
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}