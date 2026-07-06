from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service
from app.auth.schemas import RegisterRequest, RegisterResponse
from app.auth.service import AuthService

from app.account.models import Account
from app.account.schemas import AccountResponse
from app.auth.dependencies import (
    get_auth_service,
    get_current_account,
)

from app.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.register(data)

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.login(data)

@router.get(
    "/me",
    response_model=AccountResponse,
)
def me(
    current_account: Account = Depends(get_current_account),
):
    return current_account