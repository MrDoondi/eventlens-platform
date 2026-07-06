from datetime import datetime, timezone
from app.account.schemas import AccountCreate
from app.account.service import AccountService
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
)
from app.auth.security import hash_password
from app.core.exceptions import (
    AccountAlreadyExistsError,
    OrganizationNotFoundError,
)
from app.organization.service import OrganizationService

from app.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)

from app.auth.security import (
    hash_password,
    verify_password,
)

from app.core.exceptions import (
    AccountAlreadyExistsError,
    InvalidCredentialsError,
    OrganizationNotFoundError,
)


class AuthService:
    def __init__(
        self,
        account_service: AccountService,
        organization_service: OrganizationService,
    ):
        self.account_service = account_service
        self.organization_service = organization_service

    def register(
        self,
        data: RegisterRequest,
    ) -> RegisterResponse:

        organization = self.organization_service.get_by_slug(
            data.organization_slug,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        existing = self.account_service.get_by_email(
            data.email,
        )

        if existing:
            raise AccountAlreadyExistsError()

        account = self.account_service.create(
            AccountCreate(
                organization_id=organization.id,
                full_name=data.full_name,
                email=data.email,
                password_hash=hash_password(
                    data.password,
                ),
            )
        )

        access_token = create_access_token(
            str(account.id),
        )

        refresh_token = create_refresh_token(
            str(account.id),
        )

        return RegisterResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            account=account,
        )
    def login(
        self,
        data: LoginRequest,
    ) -> LoginResponse:

        account = self.account_service.get_by_email(
            data.email,
        )

        if account is None:
            raise InvalidCredentialsError()

        if not verify_password(
            data.password,
            account.password_hash,
        ):
            raise InvalidCredentialsError()
        account.last_login = datetime.now(timezone.utc)

        self.account_service.update(account)

        access_token = create_access_token(
            str(account.id),
        )

        refresh_token = create_refresh_token(
            str(account.id),
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            account=account,
        )