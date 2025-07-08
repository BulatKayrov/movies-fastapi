import uuid

from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMovieCreate, SMoviePartialUpdate, SMovieUpdate

random_name = uuid.uuid4().hex[:10]


movie = SMovieCreate(
    slug=random_name,
    title=random_name,
    description="default example description2",
    year=1990,
)


def test_create_movie() -> None:
    res = storage.create(data=movie)
    assert res.title == random_name


def test_delete_movie_by_slug() -> None:
    slugs = [value.slug for value in storage.find_all()]
    for slug in slugs:
        storage.delete_by_slug(slug)
    assert storage.find_all() == []


def test_delete_movie() -> None:
    storage.delete_record(movie)
    res = storage.find_by_slug(slug=movie.slug)
    assert res is None


def test_partial_update_movie() -> None:
    new_title = "new title"
    res = storage.create(data=movie)
    new_obj = storage.update(
        slug=res.slug, movie_in=SMoviePartialUpdate(title=new_title), partial=True
    )
    assert new_obj.title == new_title
    storage.delete_record(res)


def test_update_movie() -> None:
    res = storage.create(data=movie)
    new_data = {
        "title": "new title",
        "description": "new description",
        "year": 1990,
    }

    new_obj = storage.update_record(
        slug=res.slug, movie_in=SMovieUpdate.model_validate(new_data)
    )
    assert new_obj.title == new_data["title"]
    storage.delete_record(res)
