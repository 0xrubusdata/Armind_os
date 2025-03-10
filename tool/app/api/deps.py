from typing import Generator, Annotated
from fastapi import Depends
from app.services.talib_service import TalibService
from app.core.logging import logger

def get_talib_service() -> Generator[TalibService, None, None]:
    """
    Dependency for TalibService.
    
    Creates a new TalibService instance for each request and handles cleanup.
    
    Returns:
        Generator yielding a TalibService instance
    """
    logger.debug("Creating new TalibService instance")
    service = TalibService()
    try:
        yield service
    except Exception as e:
        logger.error(f"Error in TalibService: {str(e)}")
        raise
    finally:
        # Cleanup if needed
        logger.debug("TalibService instance released")

# Create a reusable dependency
TalibServiceDep = Annotated[TalibService, Depends(get_talib_service)]