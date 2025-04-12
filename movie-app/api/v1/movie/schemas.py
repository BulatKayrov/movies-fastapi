from pydantic import BaseModel


class SMovieBase(BaseModel):
    movie_id: int
    title: str
    description: str
    year: int


class SMovie(SMovieBase):
    pass
