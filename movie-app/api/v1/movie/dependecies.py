import logging

from api.v1.movie.auth.service import redis_auth_helper, redis_tokens_helper
from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMovie
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

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
) -> None:

    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        validate_basic(credentials=credentials)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password]",
        headers={"WWW-Authenticate": "Basic"},
    )


def find_movie_by_slug(slug: str) -> SMovie:
    film = storage.find_by_slug(slug)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film


def get_token(
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    logger.info("api token required %s", api_token)
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    validate_token(api_token)


def validate_token(api_token: HTTPAuthorizationCredentials) -> None:
    if redis_tokens_helper.token_exists(api_token.credentials):
        return None
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
    )


def validate_basic(credentials: HTTPBasicCredentials) -> None:
    if credentials and redis_auth_helper.validate_user_password(
        username=credentials.username, password=credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password]",
    )


def api_or_basic(
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
    credentials: HTTPBasicCredentials | None = Depends(basic_auth),
) -> None:

    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        validate_basic(credentials=credentials)

    if api_token:
        validate_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password] OR API token",
    )
