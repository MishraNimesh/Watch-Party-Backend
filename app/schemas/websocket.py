from pydantic import BaseModel


class ChatMessage(BaseModel):
    type: str = "chat"
    message: str


class PlayMessage(BaseModel):
    type: str = "play"
    position: float


class PauseMessage(BaseModel):
    type: str = "pause"
    position: float


class SeekMessage(BaseModel):
    type: str = "seek"
    position: float
    