import enum
from pydantic import BaseModel

class SocketEvent:
    open = 'socket_open'
    bot = 'bot'
    message_stream = 'main_content_socket'


class DataChunkType(str, enum.Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    bubble_id: str
    session_id: str
    data: str
    type: DataChunkType
    index: int

class PromptRole(str, enum.Enum):
    human = 'human'
    system = 'system'
    ai = 'ai'


class UniversalMessageType(BaseModel):
    role: PromptRole
    content: str


class UniversalMessageList(BaseModel):
    messages: list[UniversalMessageType]


def simple_message_convert(system_prompt: str, human_query: str):
    return UniversalMessageList(messages=[
        UniversalMessageType(role=PromptRole.system, content=system_prompt),
        UniversalMessageType(role=PromptRole.human, content=human_query),
    ])


def messages_langchain_convert(message_list: UniversalMessageList):
    return list(map(lambda x: (x.role.value, x.content), message_list.messages))


