import logging

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError

from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate, SMoviePartialUpdate
from core.config import settings

logger = logging.getLogger(__name__)


class StorageMovie(BaseModel):

    data_files: dict[str, SMovie] = {}  # {'slug': SMovie()}

    def save(self):
        settings.DB_URL.write_text(self.model_dump_json(indent=4))
        logger.info("New movie saved")

    @classmethod
    def from_statement(cls):
        if not settings.DB_URL.exists():
            return StorageMovie()
        return cls.model_validate_json(settings.DB_URL.read_text())

    def find_all(self):
        return list(self.data_files.values())

    def find_by_slug(self, slug: str):
        obj = self.data_files.get(slug)
        return obj

    def create(self, data: SMovieCreate):
        new_movie = SMovie(**data.model_dump())
        slug = new_movie.slug
        if slug not in self.data_files:
            self.data_files[slug] = new_movie
            self.save()
            logger.info("Mobie by slug created %s", slug)
            return
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie exists")

    def delete_by_slug(self, slug: str):
        self.data_files.pop(slug, None)
        self.save()

    def delete_record(self, movie: SMovie):
        self.delete_by_slug(slug=movie.slug)

    def update_record(self, movie: SMovie, movie_in: SMovieUpdate):
        for key, value in movie_in:
            setattr(movie, key, value)
        self.save()
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

        self.save()
        return movie


try:
    storage = StorageMovie.from_statement()
    logger.warning("Storage module loaded")
except ValidationError as e:
    storage = StorageMovie()
    storage.save()
    logger.warning("Storage module reloaded")
