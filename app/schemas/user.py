from pydantic import BaseModel


class UserCreate(BaseModel): #When sending a user back to the client, only expose these three fields.
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str