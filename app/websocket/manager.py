from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_code: str, websocket: WebSocket):
        await websocket.accept()

        if room_code not in self.active_connections:
            self.active_connections[room_code] = []

        self.active_connections[room_code].append(websocket)

    def disconnect(self, room_code: str, websocket: WebSocket):
        if room_code in self.active_connections:
            self.active_connections[room_code].remove(websocket)

            if not self.active_connections[room_code]:
                del self.active_connections[room_code]

async def broadcast(self, room_code: str, message: dict):
    for connection in self.active_connections.get(room_code, []):
        await connection.send_json(message)  #Sending structured data to understand what type of message it is