from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

class ExplanationSyncResponse(BaseModel):
    concept: str
    explanation: str 

class TalibContentResponse(BaseModel):
    """
    Response model for talibd content.
    """
    content: str = Field(..., description="The talibd text content")
    stop: bool = Field(False, description="Whether generation was stopped")
    stop_reason: Optional[str] = Field(None, description="Reason for stopping generation")
    model: str = Field(..., description="Model used for generation")
    created_at: str = Field(..., description="Timestamp of generation")

    def __init__(self, answer: str, explanation:ExplanationSyncResponse=None, example: str=None) -> None:
        super().__init__(answer=answer, explanation=explanation, example=example)
        self.answer = answer
        self.explanation = explanation
        self.example = example

class TalibCompleteResponse(BaseModel):
    """
    Complete response model for text generation.
    """
    response: Dict[str, Any] = Field(..., description="Raw response from the model")
    prompt: str = Field(..., description="Original prompt used for generation")
    sync: bool = Field(..., description="Whether the request was processed synchronously")
    stream: bool = Field(..., description="Whether the response is streamed")
    content: Optional[TalibContentResponse] = Field(None, description="Processed generation content")

    def __init__(self, service, model, created_at, done, done_reason, prompt, answer, context) -> None:
        super().__init__(service=service, model=model, created_at=created_at, done=done, done_reason=done_reason, prompt=prompt, answer=answer, context=context)
        self.service = service
        self.model = model
        self.created_at = created_at
        self.done = done
        self.done_reason = done_reason
        self.prompt = prompt
        self.answer = answer
        self.context = context

    service: str    
    model: str
    created_at: str
    done: bool
    done_reason: str
    prompt: str
    answer: TalibContentResponse
    context: List[int]