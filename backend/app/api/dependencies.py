from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from ..infrastructure.security.jwt import get_current_user
from ..infrastructure.db.session import get_session
from ..infrastructure.db.models import User


async def get_db_session(session: AsyncSession = Depends(get_session)) -> AsyncSession:
    return session


async def get_current_tenant_id(current_user: User = Depends(get_current_user)) -> uuid.UUID:
    return current_user.tenant_id
