from typing import Annotated

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select

from app.deps import SessionDep
from app.errors import BadCredentials, InvalidToken
from app.models import User
from app.schemas import Token
from app.security import create_access_token, read_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")    # gives /docs its Authorize button


def authenticate_user(session, name: str, password: str) -> User | None:
    user = session.scalar(select(User).where(User.name == name))
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


@router.post("/token", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = authenticate_user(session, form.username, form.password)
    if user is None:
        raise BadCredentials()
    return Token(access_token=create_access_token(user.name), token_type="bearer")


@router.get("/token-info")
def token_info(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    # Shows what is inside the token. It does not look the user up in the database.
    try:
        return read_access_token(token)
    except jwt.InvalidTokenError:
        raise InvalidToken()
