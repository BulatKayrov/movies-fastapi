from fastapi import HTTPException, status
from pydantic import BaseModel

from api.v1.movie.schemas import SMovie, SMovieCreate

DATABASE = [
    SMovie(slug="1", title="Terminator 1", description="Nice film 1", year=1999),
    SMovie(slug="2", title="Terminator 2", description="Nice film 2", year=2000),
    SMovie(slug="3", title="Terminator 3", description="Nice film 3", year=2001),
]


class StorageMovie(BaseModel):

    data_files: dict[str, SMovie] = {}  # {'slug': SMovie()}

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
            return
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie exists")

    def filling(self):
        self._run()

    def _run(self):
        for item in DATABASE:
            self.data_files[item.slug] = item


storage = StorageMovie()
storage.filling()
