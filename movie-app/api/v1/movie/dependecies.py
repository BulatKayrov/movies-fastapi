import logging

from fastapi import HTTPException, status, BackgroundTasks, Request, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.v1.movie.crud import storage
from core.config import settings

logger = logging.getLogger(__name__)
UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

static_api_token = HTTPBearer(
    auto_error=False, scheme_name="Static API token", description="Static API token"
)

basic_auth = HTTPBasic(
    scheme_name="Basic",
    description="Basic auth scheme username and password required",
    auto_error=False,
)


def basic_auth_header(credentials: HTTPBasicCredentials | None = Depends(basic_auth)):
    if (
        credentials
        and credentials.username in settings.USER_DB
        and settings.USER_DB[credentials.username] == credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password]",
        headers={"WWW-Authenticate": "Basic"},
    )


def find_movie_by_slug(slug: str):
    film = storage.find_by_slug(slug)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film


def get_token(
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
):
    logger.info("api token required %s", api_token)
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )

    if api_token.credentials not in settings.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )
    return api_token


def save_record(background_task: BackgroundTasks, request: Request):
    yield
    if request.method in UNSAFE_METHODS:
        logger.info("Saving movie record")
        background_task.add_task(storage.save())
