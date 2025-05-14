import logging

from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from api.v1.movie.crud import storage
from core.config import settings
from redis_depends import redis

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


def basic_auth_header(
    request: Request,
    credentials: HTTPBasicCredentials | None = Depends(basic_auth),
):

    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic(credentials=credentials)
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
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
):
    if request.method not in UNSAFE_METHODS:
        return
    logger.info("api token required %s", api_token)
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    return validate_token(api_token)


def save_record(background_task: BackgroundTasks, request: Request):
    yield
    if request.method in UNSAFE_METHODS:
        logger.info("Saving movie record")
        background_task.add_task(storage.save)


def validate_token(api_token: HTTPAuthorizationCredentials):
    if redis.sismember(settings.REDIS_DB_TOKENS_NAME, api_token.credentials):
        return api_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
    )


def validate_basic(credentials: HTTPBasicCredentials):
    if (
        credentials.username in settings.USER_DB
        and settings.USER_DB[credentials.username] == credentials.password
    ):
        return


def api_or_basic(
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
    credentials: HTTPBasicCredentials | None = Depends(basic_auth),
):

    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic(credentials=credentials)

    if api_token:
        return validate_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password] OR API token",
    )
