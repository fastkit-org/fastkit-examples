import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session
from app.models import User
from fastkit_core.database import get_async_db
from fastkit_core.config import ConfigManager
configuration = ConfigManager(modules=['auth'])


# ============================================================================
# User Database (uses FastKit's session)
# ============================================================================

async def get_user_db(session: Session = Depends(get_async_db)):
    """
    Get FastAPI Users database adapter.

    ⭐ Uses FastKit's get_async_db for session management!
    """
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    User manager with custom logic.

    Handles:
    - User registration
    - Password reset
    - Email verification
    - Custom hooks
    """

    reset_password_token_secret = configuration.get('auth.RESET_PASSWORD_TOKEN_SECRET')
    verification_token_secret = configuration.get('auth.VERIFICATION_TOKEN_SECRET')

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ):
        """Hook: Called after user registration."""
        print(f"✓ User {user.email} registered successfully")
        # TODO: Send welcome email
        # TODO: Create default user settings
        # TODO: Log registration event

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ):
        """Hook: Called after password reset requested."""
        print(f"✓ Password reset requested for {user.email}")
        print(f"  Reset token: {token}")
        # TODO: Send password reset email with token

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ):
        """Hook: Called after email verification requested."""
        print(f"✓ Verification requested for {user.email}")
        print(f"  Verification token: {token}")
        # TODO: Send verification email with token


async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager instance."""
    yield UserManager(user_db)


# ============================================================================
# Authentication Backend
# ============================================================================

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Get JWT authentication strategy.

    Tokens are valid for configured lifetime (default: 1 hour).
    """
    return JWTStrategy(
        secret=configuration.get('auth.JWT_TOKEN_SECRET'),
        lifetime_seconds=configuration.get('auth.JWT_LIFETIME_SECONDS', 3600)
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# ============================================================================
# FastAPI Users Instance
# ============================================================================

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# ============================================================================
# Dependencies for Routes
# ============================================================================

# Get current authenticated user (active users only)
current_active_user = fastapi_users.current_user(active=True)

# Get current superuser (admin access)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# Get current user (optional - can be None)
current_user_optional = fastapi_users.current_user(optional=True)