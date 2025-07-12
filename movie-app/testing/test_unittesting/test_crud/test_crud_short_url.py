import unittest
import uuid
from typing import ClassVar

from redis import Redis

from api.v1.movie.crud import StorageMovie
from api.v1.movie.schemas import SMovie, SMovieCreate, SMoviePartialUpdate, SMovieUpdate
from core.config import settings

_test_redis_movie = Redis(
    host=settings.TEST_REDIS_HOST,
    port=settings.TEST_REDIS_PORT,
    db=settings.TEST_REDIS_DB_SHORT_URL,
    decode_responses=True,
)

storage = StorageMovie(instance_redis=_test_redis_movie)


class TestCRUDShortUrlTestCase(unittest.TestCase):
    mock = {
        "title": "example",
        "slug": "example",
        "description": "example description",
        "year": 2025,
    }

    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete_record(movie=self.movie)

    def create_movie(self) -> SMovie:
        return storage.create(data=SMovieCreate(**self.mock))

    def test_create_short_url(self) -> None:
        self.assertEqual(self.movie.title, self.mock["title"])
        self.assertEqual(self.movie.slug, self.mock["slug"])
        self.assertEqual(self.movie.description, self.mock["description"])
        self.assertEqual(self.movie.year, self.mock["year"])

    def test_update(self) -> None:
        title = "New Title"
        year = 2000

        short_url_in = SMovieUpdate(title=title, year=year)
        short_update = storage.update_record(
            slug=self.movie.slug, movie_in=short_url_in
        )
        self.assertEqual(short_update.title, title)
        self.assertEqual(short_update.year, year)

    def test_update_partial(self) -> None:
        title = "New Title"

        short_url_in = SMoviePartialUpdate(title=title)
        short_update = storage.update(
            slug=self.movie.slug, movie_in=short_url_in, partial=True
        )
        self.assertEqual(short_update.title, title)


class MovieGetAndGetListTestCase(unittest.TestCase):
    MOVIES: ClassVar[list[SMovieCreate | SMovie]] = []

    @classmethod
    def create_short_url(cls) -> SMovie:
        return storage.create(
            SMovieCreate(
                slug=uuid.uuid4().hex[:10],
                title="example",
                year=2025,
                description="example description",
            )
        )

    @classmethod
    def setUpClass(cls) -> None:
        cls.MOVIES = [cls.create_short_url() for _ in range(5)]

    @classmethod
    def tearDownClass(cls) -> None:
        for _ in cls.MOVIES:
            storage.delete_record(movie=_)

    def test_get_list(self) -> None:
        list_movies = storage.find_all()
        self.assertIsNotNone(list_movies)
        self.assertIn(self.MOVIES[0], list_movies)

    def test_get_by_slug(self) -> None:
        expected_movie = self.MOVIES[0]
        movie = storage.find_by_slug(slug=expected_movie.slug)

        self.assertEqual(movie.title, expected_movie.title)
        self.assertEqual(movie.year, expected_movie.year)
        self.assertEqual(movie.description, expected_movie.description)
        self.assertEqual(expected_movie, movie)
