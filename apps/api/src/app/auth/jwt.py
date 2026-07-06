from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.enums import TokenType
from app.core.exceptions import AuthenticationError

settings = get_settings()


def create_token(
    subject: str,
    token_type: TokenType,
    expires_delta: timedelta,
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type.value,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(subject: str) -> str:
    return create_token(
        subject=subject,
        token_type=TokenType.ACCESS,
        expires_delta=timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


def create_refresh_token(subject: str) -> str:
    return create_token(
        subject=subject,
        token_type=TokenType.REFRESH,
        expires_delta=timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return payload

    except JWTError as exc:
        raise AuthenticationError() from exc