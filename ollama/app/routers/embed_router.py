from fastapi import APIRouter, HTTPException
from app.services.embed_service import get_sync_embed_response
from app.models.request.request_models import EmbedRequest

router = APIRouter()

@router.post("/api/embed")
def embed_endpoint(embed_request: EmbedRequest):
    try:
        return get_sync_embed_response(embed_request)
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))    