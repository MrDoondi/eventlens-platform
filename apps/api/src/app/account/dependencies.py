from fastapi import Depends
from sqlalchemy.orm import Session

from app.account.repository import AccountRepository
from app.account.service import AccountService
from app.db.database import get_db


def get_account_repository(
    db: Session = Depends(get_db),
) -> AccountRepository:
    return AccountRepository(db)


def get_account_service(
    repository: AccountRepository = Depends(
        get_account_repository,
    ),
) -> AccountService:
    return AccountService(repository)