from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """_summary_

    Args:
        plain_password (str): original password

    Returns:
        str: hashed password
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """_summary_

    Args:
        plain_password (str): original password
        hashed_password (str): hashed password

    Returns:
        bool: True: they're the same, False: they're not the same
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    """_summary_

    Args:
        user_id (str): user id

    Returns:
        str: access token
    """
    now = datetime.now(timezone.utc)

    payload = {"sub": user_id, "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """_summary_

    Args:
        token (str): access token

    Returns:
        str | None: user_id | None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
