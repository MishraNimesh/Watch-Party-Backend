from datetime import datetime
from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: int
    room_code: str
    host_id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class RoomMemberResponse(BaseModel):
    user_id: int
    username: str
    joined_at: datetime