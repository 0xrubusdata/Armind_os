from fastapi import APIRouter, HTTPException
from app.services.show_service import get_sync_show_response

router = APIRouter()

@router.post("/api/show")
def show_endpoint():
    try:
        return get_sync_show_response()
    except HTTPException as e:
        # The exception is propagated with the correct code (404 or other)
        raise e
    except Exception as e:
        # For any other type of error, return a 500 status
        raise HTTPException(status_code=500, detail=str(e))