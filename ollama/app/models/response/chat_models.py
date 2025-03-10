from pydantic import BaseModel
from typing import List, Literal, Optional, Sequence

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant', 'system', 'tool']
    content: Optional[str]
    images: Optional[str] = None 

class ChatSyncCompleteResponse(BaseModel):
    def __init__(self, service, model, created_at, done, done_reason, messages, context) -> None:
        super().__init__(service=service, model=model, created_at=created_at, done=done, done_reason=done_reason, messages=messages, context=context)
        self.service = service
        self.model = model
        self.created_at = created_at
        self.done = done
        self.done_reason = done_reason
        self.messages = messages
        self.context = context
        
    service: str    
    model: str
    created_at: str
    done: bool
    done_reason: str
    messages: List[ChatMessage]
    context: List[int]