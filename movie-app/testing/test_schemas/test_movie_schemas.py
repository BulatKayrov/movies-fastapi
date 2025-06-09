from unittest import TestCase

from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate  # type: ignore


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
