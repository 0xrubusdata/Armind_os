from fastapi import APIRouter, HTTPException
from app.services.chat_service import get_chat_response
from app.models.request.request_models import ChatRequest

router = APIRouter()

@router.post("/api/chat")
def chat_endpoint(chat_request: ChatRequest, sync: bool=True):
    try:
        return get_chat_response(chat_request, sync, False)
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/chat_stream")
def chat_endpoint(chat_request: ChatRequest, sync: bool=True):
    try:
        return get_chat_response(chat_request, sync, True)
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))        