from pydantic import BaseModel, Field
from typing import List, Optional, Union

class ExplanationSyncResponse(BaseModel):
    concept: str
    explanation: str 

class GenerateContentResponse(BaseModel):
    answer: str
    explanation: Optional[ExplanationSyncResponse]
    example: Optional[str]

    def __init__(self, answer: str, explanation:ExplanationSyncResponse=None, example: str=None) -> None:
        super().__init__(answer=answer, explanation=explanation, example=example)
        self.answer = answer
        self.explanation = explanation
        self.example = example

class GenerateCompleteResponse(BaseModel):
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
    answer: GenerateContentResponse
    context: List[int]
    
class ChatResponse(BaseModel):
    message: str
    
class EmbedResponse(BaseModel):
    embeddings: List[float]

class ShowResponse(BaseModel):
    details: str
    model_info: str        

class EmbedCompleteResponse(BaseModel):
    """
    Complete response model for text embedding.
    """
    model: str = Field(..., description="Model used for embedding")
    input: Union[str, List[str]] = Field(..., description="Input text that was embedded")
    embeddings: List[float] = Field(..., description="The embedding vectors")
    dimensions: int = Field(..., description="Number of dimensions in the embedding")        