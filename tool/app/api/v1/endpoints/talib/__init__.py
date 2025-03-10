from fastapi import APIRouter
from .overlap import router as overlap_router
from .momentum import router as momentum_router
from .volume import router as volume_router
from .volatility import router as volatility_router
from .price import router as price_router
from .cycle import router as cycle_router
from .pattern import router as pattern_router
from .statistic import router as statistic_router
from .math_transform import router as math_transform_router
from .math_operator import router as math_operator_router
from .info import router as info_router

# Create the main talib router
router = APIRouter(
    prefix="/talib",
    tags=["talib"],
    responses={
        404: {"description": "Function not found"},
        400: {"description": "Invalid parameters"},
        500: {"description": "Calculation error"}
    }
)

# Include all category routers
router.include_router(overlap_router)
router.include_router(momentum_router)
router.include_router(volume_router)
router.include_router(volatility_router)
router.include_router(price_router)
router.include_router(cycle_router)
router.include_router(pattern_router)
router.include_router(statistic_router)
router.include_router(math_transform_router)
router.include_router(math_operator_router)
router.include_router(info_router) 