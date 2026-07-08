from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, UserUpdate, UserInDB
from app.models.user_model import User
from app.api.dependencies.db_deps import get_db
router = APIRouter()
@router.post("/signup", response_model=UserInDB, responses = {
    400: {
        "description": "Email already registered",
        "content": {
            "application/json": {
                "example": {"msg": "Email already registered", "error_code": "EMAIL_ALREADY_REGISTERED"}
            }
        },
    }
})
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail={"msg": "Email already registered", "error_code": "EMAIL_ALREADY_REGISTERED"})

    # Create a new user instance
    new_user = User(
        email=user.email,
        password=user.password,  # In a real application, hash the password before storing it
        full_name=user.full_name,
        is_active=True,
        is_superuser=False,
        role=None
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{user_id}", response_model=UserInDB, responses = {
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"msg": "User not found", "error_code": "USER_NOT_FOUND"}
            }
        },
    }
})
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail={"msg": "User not found", "error_code": "USER_NOT_FOUND"})
    return user