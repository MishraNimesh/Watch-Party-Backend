from enum import member
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import Base, engine, get_db
from app.db import models
from app.schemas.user import UserCreate
from app.db.models import RoomMember, User,Room
from app.core.security import hash_password,verify_password,get_current_user,create_access_token
from app.schemas.user import UserCreate, UserResponse,UserLogin
from app.schemas.room import RoomResponse,RoomMemberResponse
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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": db_user.username}
    )

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
    db.flush()

    member = RoomMember(  #Adding host to his created room
        room_id=room.id,
        user_id=current_user.id
    )

    db.add(member)
    db.commit()
    db.refresh(room)

    return room

@app.post("/rooms/{room_code}/join")
def join_room(
    room_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(
        Room.room_code == room_code
    ).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if not room.is_active:
        raise HTTPException(
            status_code=400,
            detail="Room is inactive"
        )

    existing_member = db.query(RoomMember).filter(
        RoomMember.room_id == room.id,
        RoomMember.user_id == current_user.id
    ).first()

    if existing_member is not None:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this room"
        )

    member = RoomMember(
        room_id=room.id,
        user_id=current_user.id
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return {
        "message": "Joined room successfully",
        "room_code": room.room_code,
        "user_id": current_user.id
    }

@app.post("/rooms/{room_code}/leave")
def leave_room(
    room_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(
        Room.room_code == room_code
    ).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if not room.is_active:
        raise HTTPException(
            status_code=400,
            detail="Room is inactive"
        )

    if room.host_id == current_user.id:
        room.is_active = False

        db.commit()

        return {
            "message": "Room ended successfully"
        }

    member = db.query(RoomMember).filter(
        RoomMember.room_id == room.id,
        RoomMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=400,
            detail="User is not a member of this room"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Left room successfully"
    }

@app.get("/rooms/{room_code}/members", response_model=list[RoomMemberResponse])
def get_room_members(
    room_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(
        Room.room_code == room_code
    ).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if not room.is_active:
        raise HTTPException(
            status_code=400,
            detail="Room is inactive"
        )

    members = (
        db.query(RoomMember, User)
        .join(User, RoomMember.user_id == User.id)
        .filter(RoomMember.room_id == room.id)
        .all()
    )

    return [
        RoomMemberResponse(
            user_id=user.id,
            username=user.username,
            joined_at=member.joined_at
        )
        for member, user in members
    ]