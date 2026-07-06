from enum import Enum


class SubscriptionPlan(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class AccountRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    PHOTOGRAPHER = "photographer"
    EDITOR = "editor"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class EventType(str, Enum):
    WEDDING = "wedding"
    PRE_WEDDING = "pre_wedding"
    ENGAGEMENT = "engagement"
    RECEPTION = "reception"
    BIRTHDAY = "birthday"
    CORPORATE = "corporate"
    CONFERENCE = "conference"
    CONCERT = "concert"
    OTHER = "other"

class EventStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class PhotoStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"