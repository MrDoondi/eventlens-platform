from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.account.dependencies import get_account_service
from app.account.models import Account
from app.account.service import AccountService
from app.auth.jwt import decode_token
from app.auth.service import AuthService
from app.core.exceptions import AuthenticationError
from app.organization.dependencies import get_organization_service
from app.organization.service import OrganizationService

security = HTTPBearer()


def get_auth_service(
    account_service: AccountService = Depends(
        get_account_service,
    ),
    organization_service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> AuthService:
    return AuthService(
        account_service=account_service,
        organization_service=organization_service,
    )


def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    account_service: AccountService = Depends(
        get_account_service,
    ),
) -> Account:
    payload = decode_token(credentials.credentials)

    account_id = payload.get("sub")

    if account_id is None:
        raise AuthenticationError()

    account = account_service.get_by_id(account_id)

    if account is None:
        raise AuthenticationError()

    if not account.is_active:
        raise AuthenticationError()

    return account