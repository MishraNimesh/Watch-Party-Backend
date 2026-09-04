from sqlalchemy import DateTime, String, Boolean, ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    max_members: Mapped[int] = mapped_column(
        default=10
    )

class RoomMember(Base):
    __tablename__ = "room_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "user_id",
            name="unique_room_member"
        ),
    )

