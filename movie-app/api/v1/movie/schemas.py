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
    slug: Annotated[str, Len(min_length=1, max_length=20)]
    title: Annotated[str, Len(min_length=1, max_length=100)]
    description: Annotated[str, Len(min_length=1, max_length=100)]
    year: int = Field(..., ge=1, le=9999)


class SMovieUpdate(SMovieBase):
    pass
