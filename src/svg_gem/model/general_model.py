from pydantic import BaseModel

class StreamingInputType(BaseModel):
    session_id: str | list[str]
    socket_id: str