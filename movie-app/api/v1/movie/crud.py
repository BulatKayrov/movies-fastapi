from pydantic import BaseModel

from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate, SMoviePartialUpdate
from core.config import settings

DATABASE = [
    SMovie(slug="1", title="Terminator 1", description="Nice film 1", year=1999),
    SMovie(slug="2", title="Terminator 2", description="Nice film 2", year=2000),
    SMovie(slug="3", title="Terminator 3", description="Nice film 3", year=2001),
]


def save_movie(func):
    def wrapper(*args, **kwargs):
        database_url = settings.DATABASE
        result = func(*args, **kwargs)
        try:
            database_url.write_text(result.model_dump_json(indent=4))
        except Exception:
            pass

    return wrapper


class StorageMovie(BaseModel):

    cashed_slug = []  # uniq slug

    def find_all(self):
        return list(self.data_files.values())

    def find_by_slug(self, slug: str):
        obj = self.data_files.get(slug)
        return obj

    @save_movie
    def create(self, data: SMovieCreate):
        new_movie = SMovie(**data.model_dump())
        if new_movie.slug in self.cashed_slug:
            raise Exception(f"Slug {new_movie.slug} already exists")
        self.cashed_slug.append(new_movie.slug)
        return new_movie

    def delete_by_slug(self, slug: str):
        self.data_files.pop(slug, None)

    def delete_record(self, movie: SMovie):
        self.delete_by_slug(slug=movie.slug)

    def update_record(self, movie: SMovie, movie_in: SMovieUpdate):
        for key, value in movie_in:
            setattr(movie, key, value)
        return movie

    def update(
        self, movie: SMovie, movie_in: SMoviePartialUpdate, partial: bool = False
    ):
        """Универсальный метод обновление записи"""
        for key, value in movie_in.model_dump(
            exclude_none=partial,
            exclude_unset=partial,
        ).items():
            setattr(movie, key, value)
        return movie


storage = StorageMovie()
