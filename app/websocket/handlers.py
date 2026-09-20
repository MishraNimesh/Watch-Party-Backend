from app.schemas.websocket import (
    ChatMessage,
    PlayMessage,
    PauseMessage,
    SeekMessage
)

def validate_message(data: dict):

    if data.get("type") == "chat":
        return ChatMessage(**data)

    elif data.get("type") == "play":
        return PlayMessage(**data)

    elif data.get("type") == "pause":
        return PauseMessage(**data)

    elif data.get("type") == "seek":
        return SeekMessage(**data)

    else:
        return None