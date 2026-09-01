from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import Base, engine, get_db
from app.db import models
from app.schemas.user import UserCreate
from app.db.models import User,Room
from app.core.security import hash_password,verify_password,get_current_user,create_access_token
from app.schemas.user import UserCreate, UserResponse,UserLogin
from app.schemas.room import RoomResponse
import random,string



def generate_room_code():
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Watch Party Backend is running"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connection works"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        return {"message": "Invalid username or password"}

    if not verify_password(user.password, db_user.hashed_password):
        return {"message": "Invalid username or password"}

    access_token = create_access_token({"sub": db_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/rooms", response_model=RoomResponse)
def create_room(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = Room(
        room_code=generate_room_code(),
        host_id=current_user.id
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room