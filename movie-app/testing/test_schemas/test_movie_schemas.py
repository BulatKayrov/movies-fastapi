import uuid
from unittest import TestCase

from api.v1.movie.schemas import (  # type: ignore
    SMovie,
    SMovieCreate,
    SMoviePartialUpdate,
    SMovieUpdate,
)
from pydantic import ValidationError


class MovieCreateTestCase(TestCase):

    def test_create_movie(self) -> None:
        movie_create = SMovieCreate(
            slug="movie", title="test-title", description="test-description", year=1990
        )
        movie_out = SMovie(**movie_create.model_dump())

        self.assertEqual(movie_out.slug, movie_create.slug)
        self.assertEqual(movie_out.title, movie_create.title)
        self.assertEqual(movie_out.description, movie_create.description)
        self.assertEqual(movie_out.year, movie_create.year)


class MovieUpdateTestCase(TestCase):

    def test_update_movie(self) -> None:
        movie_update = SMovieUpdate(
            title="test-update-title",
            year=1990,
        )
        movie_out = SMovie(**movie_update.model_dump(), slug="test-slug")

        self.assertEqual(movie_out.title, movie_update.title)
        self.assertEqual(movie_out.year, movie_update.year)
        self.assertEqual(movie_out.description, movie_update.description)


class MoviePartialUpdateTestCase(TestCase):

    def test_update_movie_partial(self) -> None:
        movie_create = SMovieCreate(
            slug="movie-partial",
            title="test-partial-title",
            description="test-partial-description",
            year=1990,
        )
        movie = SMovie(**movie_create.model_dump())

        for key, value in (
            SMoviePartialUpdate()
            .model_dump(exclude_none=True, exclude_unset=True)
            .items()
        ):
            setattr(movie, key, value)

        self.assertEqual(movie.title, movie_create.title)
        self.assertEqual(movie.description, movie_create.description)
        self.assertEqual(movie.year, movie_create.year)

        for key, value in (
            SMoviePartialUpdate(title="test-partial-title")
            .model_dump(exclude_none=True, exclude_unset=True)
            .items()
        ):
            setattr(movie, key, value)

        self.assertEqual(movie.description, movie_create.description)
        self.assertEqual(movie.year, movie_create.year)


class MovieCreateSubTestCase(TestCase):

    def test_create_movie_sub(self) -> None:
        moke = [
            {
                "slug": "movie-sub",
                "title": "test-sub-title",
                "description": "description-sub",
                "year": 1990,
            },
            {
                "slug": "movie-sub" + str(uuid.uuid4()),
                "title": "test-sub-title",
                "description": "description-sub",
                "year": 1990,
            },
            {
                "slug": "movie-sub",
                "title": "test-sub-title",
                "description": "description-sub",
                "year": 1_000_000,
            },
        ]

        for data in moke:
            with self.subTest(data=data, msg="invalid year or title"):
                movie = SMovieCreate(**data)
                self.assertEqual(movie.slug, data["slug"])
                self.assertEqual(movie.title, data["title"])


class MovieRaisesTestCase(TestCase):

    def test_create_movie_raise(self) -> None:
        with self.assertRaises(ValidationError) as exc_error:
            SMovieCreate(
                slug="1234",
                title="test-title",
                description="test-description",
                year=1990,
            )

        error_detail = exc_error.exception.errors()[0]["type"]
        expected = "string_too"
        self.assertIn(expected, error_detail)

        with self.assertRaisesRegex(
            ValidationError, expected_regex="String should have at least 5 characters"
        ):
            SMovieCreate(
                slug="1234",
                title="test-title",
                description="test-description",
                year=1990,
            )

        with self.assertRaisesRegex(
            ValidationError, expected_regex="String should have at most 12 characters"
        ):
            SMovieCreate(
                slug="1234" * 12,
                title="test-title",
                description="test-description",
                year=1990,
            )
