from pydantic import BaseModel

class Message(BaseModel):
    user_input: str
    user_id: str = "default_user"