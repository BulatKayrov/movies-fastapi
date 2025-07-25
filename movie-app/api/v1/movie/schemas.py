from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field


class SMovieBase(BaseModel):
    title: str
    description: str | None = "default description"
    year: int


class SMovie(SMovieBase):
    slug: str


class SMovieCreate(SMovie):
    slug: Annotated[str, Len(min_length=5, max_length=12)]
    title: Annotated[str, Len(min_length=5, max_length=100)]
    description: Annotated[str, Len(min_length=5, max_length=100)]
    year: int = Field(..., ge=1, le=9999)


class SMovieUpdate(SMovieBase):
    pass


class SMoviePartialUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    year: int | None = None


class SMovieResponseForAdmin(SMovie):
    notes: str
