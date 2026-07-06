from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.events.repository import EventRepository
from app.events.service import EventService


def get_event_service(
    db: Session = Depends(get_db),
) -> EventService:
    repository = EventRepository(db)

    return EventService(repository)