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