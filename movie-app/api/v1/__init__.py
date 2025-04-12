from fastapi import APIRouter

from .movie.views import router as movie_router

router = APIRouter(prefix="/v1")
router.include_router(movie_router)
