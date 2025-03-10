from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union, Sequence, Literal
from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class Message(BaseModel):
    role: MessageRole
    content: str
    images: Optional[List[str]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class Tool(BaseModel):
    type: str = "function"
    function: Dict[str, Any]
    name: str
    description: str
    parameters: Dict[str, Any]

class Options(BaseModel):
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    num_ctx: Optional[int] = None
    num_predict: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    repeat_last_n: Optional[int] = None
    repeat_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    tfs_z: Optional[float] = None
    mirostat: Optional[int] = None
    mirostat_tau: Optional[float] = None
    mirostat_eta: Optional[float] = None
    seed: Optional[int] = None
    num_thread: Optional[int] = None
    num_gpu: Optional[int] = None
    num_keep: Optional[int] = None
    cache_mode: Optional[str] = None
    grammar: Optional[str] = None

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    options: Optional[Options] = None
    format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = None
    stream: Optional[bool] = True
    raw: Optional[bool] = None
    tools: Optional[List[Tool]] = Field(
        default=None,
        description="List of tools available to the model"
    )
    keep_alive: Optional[Union[float, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "model": "llama2",
                "prompt": "Calculate RSI for these prices: [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42]",
                "stream": True,
                "tools": [{
                    "type": "function",
                    "name": "talib",
                    "description": "Technical Analysis Library for financial market data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "function": {"type": "string"},
                            "real": {"type": "array", "items": {"type": "number"}},
                            "timeperiod": {"type": "integer", "default": 14}
                        },
                        "required": ["function", "real"]
                    }
                }]
            }
        }

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = True
    options: Optional[Options] = None
    format: Optional[Union[Literal["", "json"], Dict[str, Any]]] = None
    tools: Optional[List[Tool]] = Field(
        default=None,
        description="List of tools available to the model"
    )
    keep_alive: Optional[Union[float, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "model": "llama2",
                "messages": [
                    {"role": "user", "content": "Calculate RSI for these prices: [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42]"}
                ],
                "tools": [{
                    "type": "function",
                    "name": "talib",
                    "description": "Technical Analysis Library for financial market data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "function": {"type": "string"},
                            "real": {"type": "array", "items": {"type": "number"}},
                            "timeperiod": {"type": "integer", "default": 14}
                        },
                        "required": ["function", "real"]
                    }
                }]
            }
        }

class EmbedRequest(BaseModel):
    model: str
    prompt: str
    options: Optional[Options] = None
    keep_alive: Optional[Union[float, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "model": "llama2",
                "prompt": "Hello world",
                "options": {
                    "temperature": 0.7,
                    "num_ctx": 4096
                }
            }
        }

class PullRequest(BaseModel):
    name: str
    insecure: Optional[bool] = None
    stream: Optional[bool] = True

    class Config:
        schema_extra = {
            "example": {
                "name": "llama2",
                "stream": True
            }
        }