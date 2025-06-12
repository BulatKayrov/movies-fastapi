import unittest

from api.v1.movie.crud import StorageMovie
from api.v1.movie.schemas import SMovieCreate, SMoviePartialUpdate, SMovieUpdate
from core.config import settings
from redis import Redis

_test_redis_movie = Redis(
    host=settings.TEST_REDIS_HOST,
    port=settings.TEST_REDIS_PORT,
    db=settings.TEST_REDIS_DB_SHORT_URL,
    decode_responses=True,
)

storage = StorageMovie(helper=_test_redis_movie)


class TestCRUDShortUrlTestCase(unittest.TestCase):
    mock = {
        "title": "example",
        "slug": "example",
        "description": "example description",
        "year": 2025,
    }

    def setUp(self):
        self.movie = self.create_short_url()

    def tearDown(self):
        storage.delete_record(movie=self.movie)

    def create_short_url(self):
        return storage.create(data=SMovieCreate(**self.mock))

    def test_create_short_url(self):
        self.assertEqual(self.movie.title, self.mock["title"])
        self.assertEqual(self.movie.slug, self.mock["slug"])
        self.assertEqual(self.movie.description, self.mock["description"])
        self.assertEqual(self.movie.year, self.mock["year"])

    def test_update(self):
        title = "New Title"
        year = 2000

        short_url_in = SMovieUpdate(title=title, year=year)
        short_update = storage.update_record(
            slug=self.movie.slug, movie_in=short_url_in
        )
        self.assertEqual(short_update.title, title)
        self.assertEqual(short_update.year, year)

    def test_update_partial(self):
        title = "New Title"

        short_url_in = SMoviePartialUpdate(title=title)
        short_update = storage.update(
            slug=self.movie.slug, movie_in=short_url_in, partial=True
        )
        self.assertEqual(short_update.title, title)
